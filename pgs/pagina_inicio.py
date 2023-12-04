import streamlit as st

from util import get_binary_file_downloader_html


def pagina_inicio(logged: bool) -> None:
    st.image("images/portada.png", use_column_width=True)

    st.markdown(
        """
        ## Aplicación de Predicción de Viscosidad para Fabricación de Tintes de Cabello

        Bienvenido a nuestra aplicación avanzada para la predicción de la viscosidad en el proceso de fabricación de tintes de cabello. 
        Nuestro sistema utiliza tecnología punta para garantizar la calidad y consistencia de los tintes producidos. 
        A continuación, encontrarás cómo nuestra aplicación puede ayudarte a mejorar tus procesos de fabricación.

        ### Características Principales

        #### Selección y Predicción
        - **Selección del Tinte**: Elige el tipo de tinte que deseas producir y la cantidad requerida.
        - **Predicción de Viscosidad**: Calculamos la probabilidad de que la viscosidad no sea la adecuada para cada uno de los tres reactores disponibles 
        en la planta de fabricación.
        
        Hay tres reactores, grande de 3000 Kg, mediano de 1000 Kg y pequeño de 500 Kg.        
        """
    )

    if not logged:
        st.warning(
            """
            #### Inicia sesión para acceder a las funcionalidades
            """
        )

    st.markdown(
        """
        ### Archivos de la aplicación
        """
    )

    files_download = [
        {
            "ruta": "static_data/listado_tintes.txt",
            "descripcion": "Listado de tintes disponibles en la aplicación",
        },
        {
            "ruta": "static_data/componentes.csv",
            "descripcion": "Listado de cantidad de componentes por tinte para 1000 Kg de producción",
        },
    ]

    for file in files_download:
        st.markdown(
            get_binary_file_downloader_html(file["ruta"], file["ruta"].split("/")[-1]),
            unsafe_allow_html=True,
        )
        st.write(file["descripcion"])
        st.markdown("---")

    st.markdown(
        get_binary_file_downloader_html(
            "static_data/datos_entrenamiento.csv", "datos_entrenamiento.csv"
        ),
        unsafe_allow_html=True,
    )

    st.write("Datos de entrenamiento para el modelo de predicción de viscosidad")
    st.markdown(
        """
        Variables de entrada:

        - **orden** : Número de orden de fabricación
        - **fecha** : Fecha de fabricación
        - **matcode** : Código del tinte
        - **cantidad** : Cantidad de tinte a fabricar
        - **target**: Indica si la primera medición de viscosidad fue buena o mala. 0 Buena, 1 Mala
        - **reactor**: Reactor utilizado para la fabricación del tinte. (grande, medio, pequeño)

        """,
    )
