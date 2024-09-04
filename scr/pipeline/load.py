import pandas as pd
from sqlalchemy.engine.base import Engine
from scr.utils.logger_config import logger

def load(transformed_data: pd.DataFrame, db_engine: Engine) -> None:
    """
    Loads transformed data into a PostgreSQL database.

    The data is loaded into a table named 'news'. If the table already exists, it is replaced.

    Parameters
    ----------
    transformed_data : pd.DataFrame
        The DataFrame containing the transformed data to be loaded into the database.
    db_engine : sqlalchemy.engine.base.Engine
        The SQLAlchemy Engine instance connected to the PostgreSQL database.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the transformed_data DataFrame is empty.
    sqlalchemy.exc.SQLAlchemyError
        If there is an error during the loading process, it is logged and re-raised.
    """
    try:
        if transformed_data.empty:
            logger.error("The DataFrame is empty. No data to load.")
            raise ValueError("The transformed_data DataFrame is empty.")

        transformed_data.to_sql(
            name="news",
            con=db_engine,
            index=False,
            if_exists="replace"
        )
        logger.info("Data loaded successfully into the 'news' table.")
    except Exception as e:
        logger.error(f"An error occurred while loading data into the database: {e}")
        raise
