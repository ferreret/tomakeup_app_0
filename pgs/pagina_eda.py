import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from data_repo import read_data


# ----------------------------------------------------------------------------------------------------------------------
def pagina_eda(logged: bool) -> None:
    st.subheader("🔍 Análisis Exploratorio de Datos", divider="red")

    # Si no está logueado, no puede acceder a la página
    if not logged:
        st.warning(
            """
            Inicia sesión para acceder al análisis exploratorio de datos
            """
        )
        return

    st.write(
        """
        En este análisis exploratorio, indagaremos en las características clave del conjunto de datos, 
        identificando tendencias, patrones y anomalías. Utilizaremos visualizaciones gráficas para comprender 
        mejor las distribuciones y correlaciones. 
        Este proceso es fundamental para guiar nuestras decisiones de modelado y análisis estadístico, 
        asegurando una interpretación precisa y fundamentada de los datos.
        """
    )

    run_eda()


# ----------------------------------------------------------------------------------------------------------------------
def run_eda():
    eda_data = preprocess_data(
        orders_data=read_data("datos_entrenamiento.csv"),
        components_data=read_data("componentes.csv"),
    )

    target_labels = {
        0: "Viscosidad correcta",
        1: "Viscosidad incorrecta",
    }

    eda_data["resultado"] = eda_data["target"].map(target_labels)

    col_data, col_tema = st.columns([3, 1])

    with col_data:
        with st.expander("Datos de entrenamiento", expanded=False):
            st.dataframe(eda_data)
    with col_tema:
        with st.expander("Tema colores", expanded=False):
            temas_plotly = [
                "plotly",
                "plotly_white",
                "plotly_dark",
                "ggplot2",
                "seaborn",
                "simple_white",
                "none",
            ]
            tema_seleccionado = st.selectbox("", temas_plotly)
            px.defaults.template = tema_seleccionado

    # Creamos dos columnas, una con un expander con la distribución de la columna target y otro con un expander con la
    # distribución de la columna target en un gráfico de tarta
    col1, col2 = st.columns(2)

    with col1:
        with st.expander(
            "Distribución de la predicción de viscosidad en un gráfico de tarta",
            expanded=True,
        ):
            st.plotly_chart(target_distribution(eda_data), use_container_width=True)

    with col2:
        with st.expander("Descripción estádistica de los datos", expanded=True):
            descripcion_estadistica(eda_data)

    with st.expander("Distribución de la producción por  reactor", expanded=True):
        reactores(eda_data)

    with st.expander("Histográma de variables numéricas"):
        histograma_variable(eda_data)

    with st.expander("Relación entre las variables y la visocidad"):
        relacion_variable_target(eda_data)

    with st.expander("Relación entre las variables - gráfico de dispersión"):
        relacion_variable_variable(eda_data)

    with st.expander("Correlación entre las variables"):
        correlacion_variables(eda_data)


# ----------------------------------------------------------------------------------------------------------------------
def correlacion_variables(eda_data: pd.DataFrame) -> None:
    corr_matrix = eda_data.drop(columns=["fecha", "reactor", "resultado"]).corr().round(2)    

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu",
        labels=dict(x="Variable", y="Variable", color="Coeficiente de Correlación"),
        height=1200,
        width=1200,
    )

    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------------------------------------------------
def relacion_variable_variable(eda_data: pd.DataFrame) -> None:
    x_var = st.selectbox(
        "Variable eje X", eda_data.select_dtypes(include=["int64", "float64"]).columns
    )
    y_var = st.selectbox(
        "Variable eje Y", eda_data.select_dtypes(include=["int64", "float64"]).columns
    )

    fig = px.scatter(eda_data, x=x_var, y=y_var, color="resultado")

    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------------------------------------------------
def relacion_variable_target(eda_data: pd.DataFrame) -> None:
    target_variable = st.selectbox(
        "Selecciona la variable a analizar",
        eda_data.drop(columns=["target"])
        .select_dtypes(include=["int64", "float64"])
        .columns,
    )

    fig = px.box(eda_data, x="resultado", y=target_variable, points="all")
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------------------------------------------------
def descripcion_estadistica(eda_data: pd.DataFrame) -> None:
    description = eda_data.describe()
    description = description.map(lambda x: round(x, 2))
    st.dataframe(description)


# ----------------------------------------------------------------------------------------------------------------------
def reactores(eda_data: pd.DataFrame) -> None:
    st.plotly_chart(
        px.histogram(
            eda_data,
            x="reactor",
            color="resultado",
            barmode="group",
            title="Distribución de la producción por reactor",
        ),
        use_container_width=True,
    )


# ----------------------------------------------------------------------------------------------------------------------
def histograma_variable(eda_data: pd.DataFrame) -> None:
    hist_variable = st.selectbox(
        "Selecciona una variable",
        eda_data.drop(columns=["target"])
        .select_dtypes(include=["int64", "float64"])
        .columns,
    )

    st.checkbox("Mostrar por resultado de viscosidad", value=True, key="checkbox")

    if st.session_state.checkbox:
        st.plotly_chart(
            px.histogram(
                eda_data,
                x=hist_variable,
                color="resultado",
                barmode="group",
                title=f"Histograma de la variable {hist_variable}",
                labels={"target": "Resultado de viscosidad"},
            ),
            use_container_width=True,
        )
    else:
        st.plotly_chart(
            px.histogram(
                eda_data,
                x=hist_variable,
                title=f"Histograma de la variable {hist_variable}",
            ),
            use_container_width=True,
        )


# ----------------------------------------------------------------------------------------------------------------------
def target_distribution(eda_data: pd.DataFrame) -> None:
    # Gráfico de tarta con Plotly
    pie_chart = px.pie(
        eda_data,
        values=eda_data["target"].value_counts().values,
        names=["Viscosidad correcta", "Viscosidad incorrecta"],
    )
    return pie_chart


# ----------------------------------------------------------------------------------------------------------------------
@st.cache_data
def preprocess_data(
    orders_data: pd.DataFrame, components_data: pd.DataFrame
) -> pd.DataFrame:
    # Creo la columna de grado de llenado
    substitucion = {
        "grande": 3000,
        "mediano": 1000,
        "pequeño": 500,
    }

    orders_data["capacidad_reactor"] = orders_data["reactor"].map(substitucion)

    orders_data["grado_llenado"] = round(
        (orders_data["cantidad"] / orders_data["capacidad_reactor"]) * 100, 2
    )

    # st.dataframe(orders_data)

    # Reordeno las columnas para que sean ingual que en el entrenamiento
    orders_data = orders_data[
        [
            "orden",
            "fecha",
            "matcode",
            "cantidad",
            "grado_llenado",
            "target",
            "reactor",
            "capacidad_reactor",
        ]
    ]

    # Uno los dos dataframes para en análisis exploratorio
    df_join = pd.merge(
        orders_data, components_data, left_on="matcode", right_on="material", how="left"
    )

    # Eliminamos la columna material
    df_join.drop(columns=["material"], inplace=True)

    # El campo orden y matcode han de ser de tipo string
    df_join["orden"] = df_join["orden"].astype(str)
    df_join["matcode"] = df_join["matcode"].astype(str)

    # st.dataframe(df_join)

    return df_join
