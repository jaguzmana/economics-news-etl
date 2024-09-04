import pandas as pd
import os
import json
from ..utils.logger_config import logger

def extract(path: str, des_path: str) -> pd.DataFrame:
    """
    Extracts data from JSON files located in multiple subfolders, combines them into a single DataFrame, and saves it as a CSV file.

    Parameters
    ----------
    path : str
        The directory path containing subfolders with JSON files.
    des_path : str
        The destination file path where the combined CSV file will be saved.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the combined data from all JSON files.

    Raises
    ------
    Exception
        If there is an error during the extraction process, the exception is logged and re-raised.
    """
    try:
        folders = os.listdir(path)
        total_folder_paths = [f"{path}/{folder}" for folder in folders]

        raw_data = pd.DataFrame()
        for folder in total_folder_paths:
            for file in os.listdir(folder):
                try:
                    json_data = load_json(f"{folder}/{file}")
                    if len(json_data) > 0:
                        df = json_to_df(json_data)
                        raw_data = pd.concat([raw_data, df], ignore_index=True)
                except Exception as e:
                    logger.error(f"Failed to process file {file} in folder {folder}: {e}")
        
        raw_data.to_csv(des_path, index=False)
        return raw_data
    except Exception as e:
        logger.error(f"Failed to extract data from path {path}: {e}")
        raise

def load_json(path: str) -> list | dict:
    """
    Loads JSON data from a file.

    Parameters
    ----------
    path : str
        The file path of the JSON file to be loaded.

    Returns
    -------
    list or dict
        The JSON data as a list or dictionary. If an error occurs, an empty list is returned.

    Raises
    ------
    json.JSONDecodeError
        If the JSON data cannot be decoded.
    Exception
        If there is an error loading the JSON file, the exception is logged.
    """
    try:
        with open(path) as json_file:
            data = json.load(json_file)
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from file {path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Failed to load JSON from file {path}: {e}")
        return []

def json_to_df(json_data: dict) -> pd.DataFrame:
    """
    Converts JSON data into a pandas DataFrame.

    Parameters
    ----------
    json_data : dict
        The JSON data to be converted into a DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame constructed from the JSON data. If an error occurs, an empty DataFrame is returned.

    Raises
    ------
    Exception
        If there is an error during the conversion process, the exception is logged.
    """
    try:
        parsed_news_data = []

        for news in json_data:
            for key, value in news.items():
                if isinstance(value, list):
                    if len(value) > 0:
                        news[key] = value[0]
                    else:
                        news[key] = None
                else:
                    news[key] = value

            temp = []
            columns = []
            for key, value in news.items():
                temp.append(value)
                columns.append(key)
            parsed_news_data.append(temp)

        return pd.DataFrame(parsed_news_data, columns=columns)
    except Exception as e:
        logger.error(f"Failed to convert JSON to DataFrame: {e}")
        return pd.DataFrame()
