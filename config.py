from typing import Dict, Union
import toml


def load_toml_config_file(config_file_path: str) -> Union[Dict, None]:
    """
    Loads the TOML configuration file.

    Parameters:
    config_file_path (str): The path to the TOML configuration file.

    Returns:
    Union[Dict, None]: The loaded configuration as a dictionary, or None if an exception occurs.
    """
    try:
        with open(config_file_path, "r") as toml_file:
            config = toml.load(toml_file)

        return config

    except Exception as e:
        print(f"Exception loading configuration file: {e}")
        return None
