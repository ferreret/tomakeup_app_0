import pandas as pd
import streamlit as st


@st.cache_data
def get_tintes() -> list[str]:
    """
    Reads the 'tintes.txt' file from the 'data' directory.
    Each line in the file is stripped of leading/trailing whitespace and added to a list.
    The list of lines is then returned.

    Returns:
        list[str]: A list of strings, each representing a line from the 'tintes.txt' file.

    Raises:
        FileNotFoundError: If the 'tintes.txt' file is not found in the 'data' directory.
        Exception: If any other error occurs during the file reading process.
    """
    try:
        with open("static_data/listado_tintes.txt") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        st.error("No se encontró el archivo tintes.txt")
        return []
    except Exception as e:
        st.error(f"Error desconocido: {e}")
        return []


@st.cache_data
def read_data(file_name: str) -> pd.DataFrame:
    """
    Reads a specified .csv file from the 'data' directory and returns it as a pandas DataFrame.

    Args:
        file_name (str): The name of the .csv file to read.

    Returns:
        pd.DataFrame: A DataFrame representing the specified .csv file.
    """
    return pd.read_csv(f"static_data/{file_name}")