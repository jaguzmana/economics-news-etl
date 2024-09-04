import pandas as pd
from dateparser import DateDataParser
from datetime import date
from scr.utils.logger_config import logger

def transform(raw_data: pd.DataFrame, des_path: str) -> pd.DataFrame:
    """
    Transforms raw data by cleaning and formatting it, then saves the transformed data to a CSV file.

    Parameters
    ----------
    raw_data : pd.DataFrame
        The raw data DataFrame to be transformed.
    des_path : str
        The destination file path where the transformed CSV file will be saved.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the cleaned and transformed data.

    Raises
    ------
    Exception
        If an error occurs during the transformation process, the exception is logged and re-raised.
    """
    try:
        # Drop duplicates and dropna
        transformed_data = raw_data.drop_duplicates().dropna()
        logger.info("Dropped duplicates and NaN values.")

        # Transforming title
        transformed_data['title'] = transformed_data['title'].apply(lambda x: x.replace("\n", "").strip())
        logger.info("Transformed 'title' column.")

        # Transforming lead
        transformed_data['lead'] = transformed_data['lead'].apply(lambda x: x.replace("\n", "").strip())
        logger.info("Transformed 'lead' column.")

        # Transforming author
        transformed_data['author'] = transformed_data['author'].apply(lambda x: x.replace("\n", "").strip())
        logger.info("Transformed 'author' column.")

        # Transforming url
        transformed_data['url'] = transformed_data['url'].apply(lambda x: x.replace("https://", "").strip())
        logger.info("Transformed 'url' column.")

        # Transforming date
        transformed_data['date'] = transformed_data['date'].apply(lambda x: x.replace("\xa0m", "m").strip())
        logger.info("Transformed 'date' column.")

        # Adding Newspaper name
        transformed_data['newspaper'] = transformed_data["url"].apply(get_newspaper_name)
        logger.info("Added 'newspaper' column based on 'url'.")

        # Formatting date
        transformed_data['date'] = transformed_data['date'].astype(str)
        transformed_data['date'] = transformed_data['date'].apply(date_parser)
        transformed_data['date'] = pd.to_datetime(transformed_data['date'])
        logger.info("Formatted 'date' column.")

        # Sorting by Date
        transformed_data = transformed_data.sort_values(by=["date"])
        logger.info("Sorted data by 'date' column.")

        # Saving a CSV Copy
        transformed_data.to_csv(des_path, index=False)
        logger.info(f"Saved transformed data to {des_path}.")

        return transformed_data
    except Exception as e:
        logger.error(f"An error occurred during the transformation process: {e}")
        raise

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

    Raises
    ------
    None
    """
    if "eltiempo.com" in url:
        return "El Tiempo"
    elif "larepublica.co" in url:
        return "La República"
    elif "elespectador.com" in url:
        return "El Espectador"
    else:
        logger.warning(f"Unrecognized URL format: {url}")
        return "Unknown"

def date_parser(row: str) -> date:
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

    Raises
    ------
    None
    """
    ddp = DateDataParser(languages=['es'])
    news_date = ddp.get_date_data(row)

    if news_date is not None and news_date.date_obj is not None:
        return date(news_date.date_obj.year, news_date.date_obj.month, news_date.date_obj.day)
    else:
        logger.warning(f"Failed to parse date: {row}")
        return None
