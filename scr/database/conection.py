from decouple import config
from sqlalchemy import create_engine, URL
from sqlalchemy.exc import OperationalError
from scr.utils.logger_config import logger

def get_connection():
    """
    Establishes and returns a connection to a PostgreSQL database using SQLAlchemy.

    The database credentials and other connection details are fetched from environment variables.
    Logs the connection process and any errors encountered.

    Returns
    -------
    sqlalchemy.engine.base.Engine
        A SQLAlchemy Engine instance connected to the specified PostgreSQL database.

    Raises
    ------
    decouple.UndefinedValueError
        If any of the required environment variables are not set.
    sqlalchemy.exc.OperationalError
        If there is an issue connecting to the database (e.g., wrong credentials, database not running).
    """
    try:
        db_url = URL.create(
            "postgresql+psycopg2",
            username=config("POSTGRES_USER"),
            password=config("POSTGRES_PW"),
            host="localhost",
            database=config("POSTGRES_DB_ETL_1"),
        )
        engine = create_engine(db_url)
        logger.info("Database connection successfully created.")
        return engine
    except OperationalError as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise
    except Exception as e:
        logger.error(f"An error occurred while creating the database connection: {e}")
        raise
