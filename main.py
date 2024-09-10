from scr.pipeline.extract import extract
from scr.pipeline.transform import transform
from scr.pipeline.load import load
from scr.database.conection import get_connection
from scr.utils.logger_config import logger
from scr.utils.config_storage import config_storage
from decouple import config

def main() -> None:
    try:
        logger.info("Starting Extract Data Process")
        raw_economics_news = extract(config("DATA_LOCATION"),config("DATA_LOCATION_STG_EXTRACTED"))
        logger.info("Extract Data Process Ended")
    except Exception as e:
        logger.error(f"An error occurred during the extract process: {e}")
        return

    try:
        logger.info("Starting Transform Data Process")
        transformed_economics_news = transform(raw_economics_news,config("DATA_LOCATION_STG_TRANSFORMED"))
        logger.info("Transform Data Process Ended")
    except Exception as e:
        logger.error(f"An error occurred during the transform process: {e}")
        return

    try:
        logger.info("Starting Load Data Process")
        load(transformed_economics_news, get_connection())
        logger.info("Load Data Process Ended")
    except Exception as e:
        logger.error(f"An error occurred during the load process: {e}")
        return

if __name__ == '__main__':
    config_storage()
    main()
