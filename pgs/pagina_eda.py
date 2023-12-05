import pandas as pd
import plotly.express as px
import streamlit as st

from data_repo import read_data


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

    if st.button("Iniciar análisis exploratorio de datos"):
        with st.spinner("Creando análisis exploratorio de datos..."):
            run_eda()

        st.balloons()


def run_eda():
    eda_data = preprocess_data(
        orders_data=read_data("datos_entrenamiento.csv"),
        components_data=read_data("componentes.csv"),
    )

    with st.expander("Datos de entrenamiento", expanded=False):
        st.dataframe(eda_data)

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
        pass


def target_distribution(eda_data: pd.DataFrame) -> None:
    # Gráfico de tarta con Plotly
    pie_chart = px.pie(
        eda_data,
        values=eda_data["target"].value_counts().values,
        names=["Viscosidad correcta", "Viscosidad incorrecta"],
    )
    return pie_chart


def preprocess_data(
    orders_data: pd.DataFrame, components_data: pd.DataFrame
) -> pd.DataFrame:
    # Creo la columna de grado de llenado
    substitucion = {
        "grande": 3000,
        "mediano": 1000,
        "pequeño": 500,
    }
    orders_data["grado_llenado"] = round(
        (orders_data["cantidad"] / orders_data["reactor"].map(substitucion)) * 100, 2
    )

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

    return df_join
