import pandas as pd
import plotly.express as px

import streamlit as st


from constants import EDA_DESCRIPTION, PLOTLY_THEMES
from data_repo import preprocess_data_eda, read_data


# ----------------------------------------------------------------------------------------------------------------------
def check_logged_in() -> bool:
    """
    Check if the user is logged in.

    Returns:
        bool: True if the user is logged in, False otherwise.
    """
    if not st.session_state["logged"]:
        st.warning("Inicia sesión para acceder al análisis exploratorio de datos")
        return False
    return True


# ----------------------------------------------------------------------------------------------------------------------
def pagina_eda() -> None:
    st.subheader("🔍 Análisis Exploratorio de Datos", divider="red")

    if not check_logged_in():
        return

    st.write(EDA_DESCRIPTION)

    eda_data = preprocess_data_eda()
    eda_data["resultado"] = eda_data["target"].map(
        {0: "Viscosidad correcta", 1: "Viscosidad incorrecta"}
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        with st.expander("Datos de entrenamiento"):
            st.dataframe(eda_data)
    with col2:
        with st.expander("Tema colores"):
            tema_seleccionado = st.selectbox("", PLOTLY_THEMES)
            px.defaults.template = tema_seleccionado

    # Creamos dos columnas, una con un expander con la distribución de la columna target y otro con un expander con la
    # distribución de la columna target en un gráfico de tarta
    col1, col2 = st.columns(2)

    with col1:
        with st.expander(
            "Distribución de la predicción de viscosidad en un gráfico de tarta",
            expanded=True,
        ):
            st.plotly_chart(
                plot_target_distribution(eda_data), use_container_width=True
            )

    with col2:
        with st.expander("Descripción estádistica de los datos", expanded=True):
            plot_descripcion_estadistica(eda_data)

    with st.expander("Distribución de la producción por  reactor", expanded=True):
        plot_distribucion_reactores(eda_data)

    with st.expander("Histográma de variables numéricas"):
        plot_histograma_variable(eda_data)

    with st.expander("Relación entre las variables y la visocidad"):
        plot_relacion_variable_target(eda_data)

    with st.expander("Relación entre las variables - gráfico de dispersión"):
        plot_relacion_variable_variable(eda_data)

    with st.expander("Correlación entre las variables"):
        plot_correlacion_variables(eda_data)
    # run_eda()


# ----------------------------------------------------------------------------------------------------------------------
def plot_correlacion_variables(eda_data: pd.DataFrame) -> None:
    """
    Muestra una matriz de correlación de las variables numéricas del DataFrame proporcionado.
    Args:
        eda_data (pd.DataFrame): DataFrame que contiene los datos para el análisis.
    """

    # Verifica que las columnas a excluir existan en el DataFrame
    columns_to_drop = [
        col for col in ["fecha", "reactor", "resultado"] if col in eda_data.columns
    ]
    corr_matrix = eda_data.drop(columns=columns_to_drop).corr().round(2)

    # Crea un mapa de calor para visualizar la matriz de correlación
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu",
        labels=dict(x="Variable", y="Variable", color="Coeficiente de Correlación"),
    )

    # Muestra la figura en Streamlit ajustándose al ancho del contenedor
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------------------------------------------------
def plot_relacion_variable_variable(eda_data: pd.DataFrame) -> None:
    """
    Crea y muestra un gráfico de dispersión para dos variables seleccionadas por el usuario.

    El gráfico de dispersión permite explorar la relación entre dos variables numéricas. El usuario
    elige las variables para los ejes X e Y a través de dos selectboxes en la interfaz de Streamlit.

    Args:
        eda_data (pd.DataFrame): DataFrame que contiene los datos para el análisis.
    """

    # Seleccionar variables para los ejes X e Y
    numeric_columns = eda_data.select_dtypes(include=["int64", "float64"]).columns
    x_var = st.selectbox("Variable eje X", numeric_columns)
    y_var = st.selectbox("Variable eje Y", numeric_columns)

    # Crear gráfico de dispersión con Plotly
    fig = px.scatter(
        eda_data,
        x=x_var,
        y=y_var,
        color="resultado",  # Categoriza los puntos por el campo 'resultado'
        size_max=15,  # Tamaño máximo para los marcadores
        opacity=0.5,  # Opacidad de los marcadores
    )
    fig.update_traces(marker={"size": 15})  # Tamaño de los marcadores en el gráfico

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------------------------------------------------
def plot_relacion_variable_target(eda_data: pd.DataFrame) -> None:
    """
    Crea y muestra un gráfico de caja (boxplot) para explorar la relación entre una variable objetivo
    y otra variable numérica seleccionada por el usuario.

    Esta visualización es útil para identificar tendencias, outliers y distribuciones en los datos en relación
    con la variable objetivo.

    Args:
        eda_data (pd.DataFrame): DataFrame que contiene los datos para el análisis.
    """

    # Seleccionar la variable numérica para analizar su relación con la variable objetivo
    numeric_columns = eda_data.select_dtypes(include=["int64", "float64"]).columns
    target_variable = st.selectbox(
        "Selecciona la variable a analizar",
        numeric_columns[numeric_columns != "target"],
    )

    # Crear y configurar el gráfico de caja
    fig = px.box(
        eda_data,
        x="resultado",
        y=target_variable,
        points="all",  # Muestra todos los puntos de datos
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------------------------------------------------
def plot_descripcion_estadistica(eda_data: pd.DataFrame) -> None:
    """
    Muestra un resumen estadístico del DataFrame proporcionado.

    La función calcula estadísticas descriptivas como media, desviación estándar, mínimo,
    máximo y los percentiles para todas las columnas numéricas del DataFrame, y luego muestra
    estos datos en forma de tabla en Streamlit.

    Args:
        eda_data (pd.DataFrame): DataFrame que contiene los datos para el análisis.
    """

    # Calcular estadísticas descriptivas y redondear a 2 decimales
    description = eda_data.describe().round(2)

    # Mostrar el resumen estadístico en Streamlit
    st.dataframe(description)


# ----------------------------------------------------------------------------------------------------------------------
def plot_distribucion_reactores(eda_data: pd.DataFrame) -> None:
    """
    Crea y muestra un histograma que ilustra la distribución de la producción por tipo de reactor.

    El histograma categoriza los datos por el tipo de reactor y los colorea según el resultado
    (campo 'resultado' en el DataFrame). Esta visualización ayuda a identificar patrones o tendencias
    en la distribución de la producción entre diferentes reactores.

    Args:
        eda_data (pd.DataFrame): DataFrame que contiene los datos para el análisis.
    """

    # Crear y configurar el histograma
    fig = px.histogram(
        eda_data,
        x="reactor",  # Variable para el eje X
        color="resultado",  # Categoriza los datos por 'resultado'
        barmode="group",  # Modo de agrupamiento para las barras
        title="Distribución de la producción por reactor",  # Título del gráfico
    )

    # Mostrar el histograma en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------------------------------------------------
def plot_histograma_variable(eda_data: pd.DataFrame) -> None:
    """
    Crea y muestra un histograma para una variable numérica seleccionada por el usuario.

    El usuario puede elegir una variable numérica del DataFrame y decidir si quiere visualizar
    el histograma segmentado por el resultado de la viscosidad. Esto proporciona una visión
    sobre la distribución de la variable seleccionada y, opcionalmente, cómo se relaciona con
    el resultado de la viscosidad.

    Args:
        eda_data (pd.DataFrame): DataFrame que contiene los datos para el análisis.
    """

    # Seleccionar una variable numérica para el histograma
    numeric_columns = eda_data.select_dtypes(include=["int64", "float64"]).columns
    hist_variable = st.selectbox("Selecciona una variable", numeric_columns)

    # Opción para segmentar por resultado de viscosidad
    segment_by_result = st.checkbox("Mostrar por resultado de viscosidad", value=True)

    # Crear y configurar el histograma
    histogram_params = {
        "data_frame": eda_data,
        "x": hist_variable,
        "title": f"Histograma de la variable {hist_variable}",
    }

    if segment_by_result:
        histogram_params["color"] = "resultado"
        histogram_params["barmode"] = "group"
        histogram_params["labels"] = {"target": "Resultado de viscosidad"}

    fig = px.histogram(**histogram_params)

    # Mostrar el histograma en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------------------------------------------------
def plot_target_distribution(eda_data: pd.DataFrame) -> px.pie:
    """
    Crea un gráfico de tarta que muestra la distribución de las categorías de la variable objetivo 'target'.

    El gráfico de tarta facilita la visualización de la proporción entre diferentes categorías en la
    variable 'target'. Por ejemplo, puede mostrar la proporción de resultados de viscosidad correcta
    versus incorrecta en un conjunto de datos.

    Args:
        eda_data (pd.DataFrame): DataFrame que contiene los datos, incluyendo la columna 'target'.

    Returns:
        plotly.graph_objs._figure.Figure: Un objeto de figura de Plotly que representa el gráfico de tarta.
    """

    # Calcula el conteo de valores para la variable objetivo
    target_counts = eda_data["target"].value_counts()

    # Crea el gráfico de tarta
    pie_chart = px.pie(
        names=target_counts.index,  # Nombres de las categorías
        values=target_counts.values,  # Valores correspondientes a cada categoría
        title="Distribución del objetivo 'target'",  # Título del gráfico
    )

    # Asigna nombres más descriptivos a las categorías
    pie_chart.update_traces(labels=["Viscosidad correcta", "Viscosidad incorrecta"])

    return pie_chart
