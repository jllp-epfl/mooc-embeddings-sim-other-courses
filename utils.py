from typing import Dict, Union
import pandas as pd
import json
import re


def truncate_name(course_name: str, name_max_len: int) -> str:
    """
    Truncates the given course name to a specified maximum length while preserving the number.

    Args:
        course_name (str): The name of the course to be truncated.
        name_max_len (int): The maximum length allowed for the truncated name.

    Returns:
        str: The truncated course name with the preserved trailing number or roman numeral,
             followed by "..."
    """

    if len(course_name) <= name_max_len:
        return course_name + "     "

    roman_pattern = r"(IX|IV|V?I{0,3})$"
    number_pattern = r"([1-9])$"

    roman_match = re.search(roman_pattern, course_name)
    number_match = re.search(number_pattern, course_name)

    if roman_match:
        truncated_course_name = course_name[:name_max_len] + roman_match.group(1)
    elif number_match:
        truncated_course_name = (
            course_name[:name_max_len] + number_match.group(1) + ".."
        )
    else:
        truncated_course_name = course_name[:name_max_len] + "..."

    return truncated_course_name + "     "


def load_mooc_descriptions(mooc_descriptions_path: str) -> Union[Dict, None]:
    """
    It loads the MOOC data.

    Parameters:
    mooc_descriptions_path (str): The path to the mooc description data

    Returns:
    Union[Dict, None]: The dictionary with the MOOC data or None if there is an error loading the file
    """

    try:
        with open(mooc_descriptions_path) as json_file:
            moocs_descr = json.load(json_file)
        return moocs_descr

    except Exception as e:
        print("Error: couldn't read moocs json file")
        print(e)
        return None


def load_course_descriptions(
    course_descriptions_path: str,
) -> Union[pd.DataFrame, None]:
    """
    It loads the non-MOOC courses data.

    Parameters:
    course_descriptions_path (str): The path to the course description data

    Returns:
    Union[pd.DataFrame, None]: The Pandas Dataframe with the course data or None if there is an error loading the file
    """
    try:
        df = pd.read_csv(course_descriptions_path, index_col=0).drop_duplicates()
        df = df.sort_index(ascending=True)
        return df
    except Exception as e:
        print("Error: couldn't read other courses csv file")
        print(e)
        return None
