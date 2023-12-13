import pandas as pd
import streamlit as st


# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
@st.cache_data
def preprocess_data_eda():
    """
    Preprocesses the orders data by performing various transformations and merging it with components data.

    Returns:
        DataFrame: The preprocessed data with additional columns and merged data.
    """
    orders_data = read_data("datos_entrenamiento.csv")
    components_data = read_data("componentes.csv")

    substitucion = {
        "grande": 3000,
        "mediano": 1000,
        "pequeño": 500,
    }

    orders_data["capacidad_reactor"] = orders_data["reactor"].map(substitucion)
    orders_data["grado_llenado"] = (
        (orders_data["cantidad"] / orders_data["capacidad_reactor"]) * 100
    ).round(2)

    df_join = pd.merge(
        orders_data, components_data, left_on="matcode", right_on="material", how="left"
    )
    df_join.drop(columns=["material"], inplace=True)
    df_join["orden"] = df_join["orden"].astype(str)
    df_join["matcode"] = df_join["matcode"].astype(str)

    return df_join
