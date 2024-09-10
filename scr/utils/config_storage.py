import os

def config_storage() -> None:
    """
    Configure storage by creating necessary data directories if they do not already exist.

    This function checks for the presence of the main data directory (`./scr/data/`) and 
    two subdirectories: `staging_extracted_data` and `staging_transformed_data`. 
    If these directories do not exist, the function creates them.

    The following directories will be created:
    
    - `./scr/data/`: Main data directory.
    - `./scr/data/staging_extracted_data/`: Directory for storing extracted data.
    - `./scr/data/staging_transformed_data/`: Directory for storing transformed data.

    Returns
    -------
    None
        This function does not return any value.
    """

    if not os.path.exists('./scr/data/'):
        # Creating main data folder 
        os.mkdir('./scr/data/')
        
        # Creating folder for extracted data
        os.mkdir('./scr/data/staging_extracted_data/')
        
        # Creating folder for transformed data
        os.mkdir('./scr/data/staging_transformed_data/')
