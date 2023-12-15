import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from constants import CAPACIDAD_REACTORES
from data_repo import get_tintes, read_data
from logger_config import logger


# ----------------------------------------------------------------------------------------------------------------------
def pagina_prediccion() -> None:
    """
    Function to display the prediction page for viscosity based on component proportions.

    Parameters:
    - logged (bool): Indicates whether the user is logged in or not.

    Returns:
    None
    """
    st.subheader(
        ":test_tube: Predicción viscosidad por proporción de componentes", divider="red"
    )

    if not st.session_state["logged"]:
        st.warning("Inicia sesión para acceder a la predicción")
        return

    # Creo dos columnas para aprovechar el espacio,
    # quiero que la primera columna tenga el doble de ancho que la segunda
    col1, col2 = st.columns([2, 1])

    # En la primera columna, creo un selectbox para elegir el tinte
    with col1:
        tinte = st.selectbox("Selección de tinte", get_tintes())
    with col2:
        cantidad = st.number_input(
            "Cantidad de tinte a producir (Kg):",
            min_value=1,
            max_value=3000,
            value=1,
            step=1,
        )

    # Creo un slider para el rango de proporciones de los componentes
    rango = st.slider(
        "Rango de cantidad de tinte %:",
        min_value=0,
        max_value=50,
        value=0,
        step=1,
    )

    # Pongo un botón para ejecutar la predicción alineado a la derecha
    if st.button("Predecir"):
        # Creo un spinner para mostrar que se está ejecutando la predicción
        with st.spinner("Prediciendo..."):
            try:
                # Ejecuto la predicción
                run_prediccion(tinte, cantidad, rango)
                # Muestro animación de éxito
                st.balloons()
            except Exception as e:
                # Si ocurre un error, muestro un mensaje de error
                logger.error(f"Error: {e}")
                st.error("Ocurrió un error al ejecutar la predicción")
                st.error(f"Error: {e}")


# ----------------------------------------------------------------------------------------------------------------------
def grado_llenado(cantidad: int, show_warning=True) -> tuple[float, float, float]:
    """En esta función validamos la cantidad de tinte a producir,
    a su vez, devolveremos el grado de llenado para cada uno de los reactores.

    Args:
        cantidad (int): Cantidad de tinte a producir en Kg

    Returns:
        tuple[float, float, float]: Grado de llenado para cada uno de los reactores, grande, mediano, pequeño

    """
    grados_llenado = {}
    for reactor, capacidad in CAPACIDAD_REACTORES.items():
        if cantidad <= capacidad:
            grados_llenado[reactor] = round((cantidad / capacidad) * 100, 2)
        else:
            grados_llenado[reactor] = 0
            if show_warning:
                st.warning(
                    f"La cantidad de tinte a producir supera la capacidad del reactor {reactor}"
                )

    return (
        grados_llenado["grande"],
        grados_llenado["mediano"],
        grados_llenado["pequeño"],
    )


# ----------------------------------------------------------------------------------------------------------------------
def crear_df_reactores(
    components: pd.DataFrame, grados_llenado: tuple[float, float, float], cantidad: int
) -> list[pd.DataFrame]:
    """
    Genera una lista de DataFrames con características adicionales para cada reactor.

    :param components: DataFrame con los componentes.
    :param grados_llenado: Tuple con los grados de llenado para cada reactor.
    :param cantidad: Cantidad a añadir en cada DataFrame.
    :return: Lista con tres DataFrames, uno para cada reactor.
    """
    # Nombres de las columnas adicionales
    columnas_reactor = ["reactor_mediano", "reactor_pequeño"]

    # Inicializar los DataFrames resultantes
    dfs = []

    for i, grado_llenado in enumerate(grados_llenado):
        df_temp = components.copy()
        # Establecer las columnas del reactor
        df_temp["reactor_mediano"] = int(i == 1)
        df_temp["reactor_pequeño"] = int(i == 2)
        # Añadir grado de llenado y cantidad
        df_temp["grado_llenado"] = grado_llenado
        # En el caso que el grado de llenado sea 0, el dataframe es None
        if grado_llenado == 0:
            dfs.append(None)
            continue
        df_temp["cantidad"] = cantidad
        # Reordenar las columnas
        columnas_ordenadas = ["cantidad", "grado_llenado"] + [
            col for col in df_temp.columns if col not in ["cantidad", "grado_llenado"]
        ]
        dfs.append(df_temp[columnas_ordenadas])

    return dfs


# ----------------------------------------------------------------------------------------------------------------------
def mostrar_resultado_sin_rango(dfs: list[pd.DataFrame], tinte: str) -> None:
    """
    Muestra la probabilidad de viscosidad para un tinte dado.

    Parameters
    ----------
    dfs : list[pd.DataFrame]
        Una lista de DataFrames que contienen información sobre la probabilidad de viscosidad para el tinte dado.
    tinte : str
        El nombre del tinte para el cual se desea mostrar la probabilidad de viscosidad.

    Returns
    -------
    None
    """
    st.markdown(f"**Probabilidad de viscosidad para el tinte {tinte}**")
    # Concatenamos los DataFrames
    df = pd.concat(dfs)
    # Ordenamos por probabilidad descendente
    df = df.sort_values(by=["probabilidad"])

    # Si reactor_mediano y reactor_pequeño son 0, creamos una columna de nombre reactor que tenga el valor Grande
    # Si reactor_mediano es 1, creamos una columna de nombre reactor que tenga el valor Mediano
    # Si reactor_pequeño es 1, creamos una columna de nombre reactor que tenga el valor Pequeño
    df["reactor"] = df.apply(
        lambda x: ["Grande", "Mediano", "Pequeño"][
            int(x["reactor_mediano"]) + int(x["reactor_pequeño"]) * 2
        ],
        axis=1,
    )

    for i, row in enumerate(df.itertuples(index=False)):
        message = f"Reactor {row.reactor}: {row.probabilidad:.2f}% de probabilidad de viscosidad negativa"
        if i == 0:
            st.success(message)
            logger.info(message)
        else:
            st.info(message)


# ----------------------------------------------------------------------------------------------------------------------
def mostrar_resultado_con_rango(
    dfs: list[pd.DataFrame], tinte: str, variable: str
) -> None:
    """
    Plots the probability of negative viscosity for a given dye, based on the amount produced,
    and prints the minimum probability for each reactor with the corresponding variable value.

    Args:
        dfs (list[pd.DataFrame]): A list of pandas DataFrames containing the probability of negative viscosity
            for each reactor, sorted by the amount of dye produced.
        tinte (str): The name of the dye being produced.
    """
    # Ordenamos por cantidad y preparamos los trazos de los gráficos
    trazos = []
    nombres_reactores = ["Reactor Grande", "Reactor Mediano", "Reactor Pequeño"]

    for i, df in enumerate(dfs):
        if df is not None:
            df_sorted = df.sort_values(by=[variable])
            dfs[i] = df_sorted

            # Agregar trazo al gráfico
            trazo = go.Scatter(
                x=df_sorted[variable],
                y=df_sorted["probabilidad"],
                mode="lines",
                name=nombres_reactores[i],
            )
            trazos.append(trazo)

            # Encontrar el mínimo de probabilidad y el valor correspondiente de la variable
            min_prob = df_sorted["probabilidad"].min()
            valor_variable_min_prob = df_sorted[df_sorted["probabilidad"] == min_prob][
                variable
            ].iloc[0]

            # Mostrar esta información
            logger.info(
                f"{nombres_reactores[i]}: Probabilidad mínima de {min_prob}% a {valor_variable_min_prob} Kg de {tinte}"
            )

    # Crear figura con los trazos
    fig = go.Figure(data=trazos)
    fig.update_layout(
        title=f"Probabilidad de viscosidad para el tinte {tinte}",
        xaxis_title=f"{variable} (Kg)",
        yaxis_title="Probabilidad de viscosidad negativa (%)",
        legend_title="Reactor",
    )

    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------------------------------------------------
def predecir_viscosidad(
    dfs: list[pd.DataFrame],
    model,
    variable: str,
    valor_medio: float,
    rango: int,
):
    """
    Predice la probabilidad de viscosidad para cada reactor y actualiza los DataFrames.

    :param dfs: Lista de DataFrames correspondientes a cada reactor.
    :param model: Modelo para la predicción.
    :param variable: Nombre de la variable a aplicar el rango
    :param valor_medio: Valor medio de la variable a crear el rango
    :param rango: Rango de variación de la variable.
    :param grado_llenado: Función para calcular el grado de llenado.
    """
    for i, df in enumerate(dfs):
        if df is not None:
            # Predecir probabilidad inicial
            df["probabilidad_valor_medio"] = (
                model.predict_proba(df)[:, 1] * 100
            ).round(2)

            if rango > 0:
                for j in range(int(valor_medio) - rango, int(valor_medio) + rango + 1):
                    if (
                        i == 0
                        or (
                            j <= CAPACIDAD_REACTORES[["mediano", "pequeño"][i - 1]]
                            and variable == "cantidad"
                        )
                    ) or variable != "cantidad":
                        df_temp = df.copy()
                        if variable == "cantidad":
                            df_temp[variable] = j
                            df_temp["grado_llenado"] = grado_llenado(
                                j, show_warning=False
                            )[i]
                        else:
                            df_temp[variable] = j

                        # Concatenar con el DataFrame principal
                        dfs[i] = pd.concat([dfs[i], df_temp])

            # Calcular la probabilidad final
            dfs[i]["probabilidad"] = (
                model.predict_proba(dfs[i].drop(columns=["probabilidad_valor_medio"]))[
                    :, 1
                ]
                * 100
            ).round(2)

    return dfs


# ----------------------------------------------------------------------------------------------------------------------
def run_prediccion(tinte: str, cantidad: int, rango: int) -> None:
    """
    Runs the prediction process for a given tinte, cantidad, and rango.

    Args:
        tinte (str): The selected tinte.
        cantidad (int): The amount of tinte.
        rango (int): The range of prediction.

    Returns:
        None
    """

    logger.info(
        f"Predicción para el tinte {tinte} con {cantidad} Kg con rango {rango} %"
    )

    componentes_df = read_data("componentes.csv")
    # Rest of the code...

    # Selecciono el tinte que se eligió en el selectbox
    # y filtro el DataFrame de componentes por ese tinte
    componentes_df = componentes_df.loc[
        componentes_df["material"] == int(tinte[:6])
    ].drop("material", axis=1)

    # Compruebo que el DataFrame de componentes no esté vacío
    if componentes_df.empty:
        logger.error("No se encontraron componentes para el tinte seleccionado")
        st.error("No se encontraron componentes para el tinte seleccionado")
        return

    # Calculo el grado de llenado para cada uno de los reactores
    grados_llenado = grado_llenado(cantidad)
    # Creo los DataFrames para cada reactor
    dfs = crear_df_reactores(componentes_df, grados_llenado, cantidad)
    # Cargamos el modelo
    loaded_model = joblib.load("models/xgb_viscosity.joblib")

    if rango == 0:
        predecir_viscosidad(dfs, loaded_model, "cantidad", cantidad, rango)
        mostrar_resultado_sin_rango(dfs, tinte)
        return

    # El valor del rango es un %, lo transformamos a un valor absoluto y lo redondeamos
    rango = round(cantidad * (rango / 100))

    # Predecimos la probabilidad de viscosidad para cada reactor
    dfs = predecir_viscosidad(dfs, loaded_model, "cantidad", cantidad, rango)
    mostrar_resultado_con_rango(dfs, tinte, "cantidad")
