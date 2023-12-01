import streamlit as st


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
