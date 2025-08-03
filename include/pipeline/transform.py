def transform(data):
    """
    Transforms raw data by cleaning and formatting it.

    Parameters
    ----------
    data : pd.DataFrame
        The raw data DataFrame to be transformed.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the cleaned and transformed data.
    """
    import pandas as pd

    # Transforming title
    data['title'] = data['title'].apply(lambda x: x.replace("\n", "").strip())

    # Transforming lead
    data['lead'] = data['lead'].apply(lambda x: x.replace("\n", "").strip())

    # Transforming author
    data['author'] = data['author'].apply(lambda x: x.replace("\n", "").strip())

    # Transforming url
    data['url'] = data['url'].apply(lambda x: x.replace("https://", "").strip())

    # Transforming date
    data['date'] = data['date'].apply(lambda x: x.replace("\xa0m", "m").strip())

    # Add newspaper name
    data['newspaper'] = data["url"].apply(get_newspaper_name)

    # Format date
    data['date'] = data['date'].astype(str)
    data['date'] = data['date'].apply(date_parser)
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data['date'] = data['date'].dt.strftime("%Y-%m-%d")

    # Sort by date
    data = data.sort_values(by=["date"])

    return data

def get_newspaper_name(url: str) -> str:
    """
    Determines the newspaper name based on the URL.

    Parameters
    ----------
    url : str
        The URL from which to extract the newspaper name.

    Returns
    -------
    str
        The name of the newspaper ('El Tiempo', 'La República', or 'El Espectador').
    """
    if "eltiempo.com" in url:
        return "El Tiempo"
    elif "larepublica.co" in url:
        return "La República"
    elif "elespectador.com" in url:
        return "El Espectador"
    else:
        return "Unknown"

def date_parser(row: str):
    """
    Parses a date string and returns a date object.

    Parameters
    ----------
    row : str
        The date string to be parsed.

    Returns
    -------
    date
        The parsed date object, or None if parsing fails.
    """

    from dateparser import DateDataParser
    from datetime import date

    ddp = DateDataParser(languages=['es'])
    news_date = ddp.get_date_data(row)

    if news_date is not None and news_date.date_obj is not None:
        return date(news_date.date_obj.year, news_date.date_obj.month, news_date.date_obj.day)
    else:
        return None
