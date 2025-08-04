def get_current_week_start(today) -> str:
    """
    Get the start of the current week (most recent Sunday) in DD-MM-YYYY format.

    Parameters
    ----------
    today : str
        The current date as a string.

    Returns
    -------
    str
        The date of the most recent Sunday in DD-MM-YYYY format.
    """
    import pendulum
    from datetime import timedelta
    
    today = pendulum.parse(today)
    
    # Calculate days since Sunday (0 = Monday, 6 = Sunday)
    days_since_sunday = (today.weekday() + 1) % 7
    
    # Get the most recent Sunday
    current_week_sunday = today - timedelta(days=days_since_sunday)
    
    # Format as DD-MM-YYYY to match your extracted_date format
    return current_week_sunday.strftime('%d-%m-%Y')

    