# Banner for the app -----------------------------------------------------------------------------------
HTML_BANNER = """
    <div style="background-color:red;padding:10px;border-radius:10px;margin-bottom:30px;">
    <h1 style="color:white;text-align:center;">ToMakeUp</h1>
    </div>
    """

# Página de inicio -------------------------------------------------------------------------------------

# Datos sobre archivos para descarga
FILES_TO_DOWNLOAD = [
    {
        "ruta": "static_data/listado_tintes.txt",
        "descripcion": "Listado de tintes disponibles en la aplicación",
    },
    {
        "ruta": "static_data/componentes.csv",
        "descripcion": "Listado de cantidad de componentes por tinte para 1000 Kg de producción",
    },
    {
        "ruta": "static_data/datos_entrenamiento.csv",
        "descripcion": "Datos de entrenamiento para el modelo de predicción de viscosidad",
    },
]

APP_DESCRIPTION = """
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

FEAUTURES_DESCRIPTION = """
        **Datos de entrenamiento para el modelo de predicción de viscosidad**

        Variables de entrada:

        - **orden** : Número de orden de fabricación
        - **fecha** : Fecha de fabricación
        - **matcode** : Código del tinte
        - **cantidad** : Cantidad de tinte a fabricar
        - **target**: Indica si la primera medición de viscosidad fue buena o mala. 0 Buena, 1 Mala
        - **reactor**: Reactor utilizado para la fabricación del tinte. (grande, medio, pequeño)
        """


# Página Exploración de Datos --------------------------------------------------------------------------
EDA_DESCRIPTION = """
        En este análisis exploratorio, indagaremos en las características clave del conjunto de datos, 
        identificando tendencias, patrones y anomalías. Utilizaremos visualizaciones gráficas para comprender 
        mejor las distribuciones y correlaciones. 
        Este proceso es fundamental para guiar nuestras decisiones de modelado y análisis estadístico, 
        asegurando una interpretación precisa y fundamentada de los datos.
        """

# Lista temas plotly
PLOTLY_THEMES = [
    "plotly",
    "plotly_white",
    "plotly_dark",
    "ggplot2",
    "seaborn",
    "simple_white",
    "none",
]

# Página de predicción ---------------------------------------------------------------------------------
CAPACIDAD_REACTORES = {
    "grande": 3000,
    "mediano": 1000,
    "pequeño": 500,
}
