import pandas as pd
from typing import List
import traceback
import sys


def process_columns(df: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    processed_df = df.copy()  # Create a copy to work with
    try:
        low_months = ["oct", "dec", "mar", "sep"]
        processed_df = processed_df[processed_df["default"] != "yes"]

        processed_df["month"] = processed_df["month"].apply(lambda x: "low" if x in low_months else x)
        processed_df.loc[
            processed_df["pdays"] > 27, "pdays"
        ] = 0  # turn this column into a categorical with two categories
        processed_df.loc[processed_df["campaign"] > 9] = 999  # indicator var
        processed_df["y"] = processed_df["y"].apply(lambda x: 0 if x == "no" else 1)
    except KeyError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # Extract unformatter stack traces as a list of strings
        traceback_details = traceback.format_tb(exc_traceback)
        error_line = traceback_details[-1]
        print(f"An error occurred on {error_line}:\n type: {exc_type}\n value: {exc_value}")     
    return processed_df


def encode_data(df: pd.DataFrame, dummy_cols: List[str]) -> pd.DataFrame:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        dummy_cols (List[str]): _description_

    Returns:
        pd.DataFrame: _description_
    """
    for dummy in dummy_cols:
        try:
            df[dummy] = df[dummy].astype(str)  # to allow it to be categorical
            encoded_df = pd.get_dummies(df[dummy])
            new_mapping = {}
            for col in encoded_df.columns:
                new_mapping[col] = f'{dummy}_{col}'
            encoded_df = encoded_df.rename(columns=new_mapping)
            df = pd.concat([df, encoded_df], axis=1)
        except KeyError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # Extract unformatter stack traces as a list of strings
            traceback_details = traceback.format_tb(exc_traceback)
            error_line = traceback_details[-1]
            print(f"An error occurred on {error_line}:\n type: {exc_type}\n value: {exc_value}")  
            return None
    df = df.drop(dummy_cols, axis=1)
    return df
