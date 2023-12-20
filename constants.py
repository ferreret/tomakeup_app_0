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

RUTA_MODELO = "static_data/xgb_viscosity.joblib"
RUTA_MODELO_USUARIO = "user_data/xgb_viscosity.joblib"

# Página de entrenamiento ------------------------------------------------------------------------------
RUTA_DATOS_ENTRENAMIENTO_USUARIO = "user_data/datos_entrenamiento.csv"
ARCHIVO_DATOS_ENTRENAMIENTO_USUARIO = "datos_entrenamiento.csv"
TEMP_FOLDER = "tmp"

# Tooltip para los parámetros de entrenamiento
TOOLTIP_ALPHA = """Alpha es el término de regularización L1 aplicado en los pesos del modelo. 
                Una regularización más alta reduce el sobreajuste penalizando los pesos grandes. 
                Un valor de 0.5 indica una regularización moderada que puede ayudar a mejorar la generalización
                del modelo."""
TOOLTIP_COLSAMPLE_BYTREE = """Especifica la fracción de características a considerar al construir cada árbol. 
                            Un valor de 0.9 significa que el 90% de las características se seleccionarán 
                            aleatoriamente para cada árbol, lo que ayuda a prevenir el sobreajuste
                            y añade más aleatoriedad al proceso de aprendizaje."""
TOOLTIP_GAMMA = """Gamma es el parámetro de regularización para el criterio de división de nodos. 
                Un valor más alto hace que el algoritmo sea más conservador, es decir, se requiere una ganancia
                de pérdida más significativa para realizar una división. Un valor de 0.2 es relativamente bajo, 
                permitiendo divisiones más fáciles."""
TOOLTIP_LEARNING_RATE = """Controla la magnitud de actualización de los pesos del modelo en cada paso. 
                        Un valor bajo de 0.005 hace que el modelo aprenda lentamente, reduciendo el riesgo de 
                        sobreajuste, pero puede requerir más iteraciones para converger."""
TOOLTIP_MAX_DEPTH = """Determina la profundidad máxima de cada árbol. Un valor de 4 limita la complejidad
                    de los árboles, evitando el sobreajuste pero permitiendo que el modelo capture suficientes
                    interacciones entre las características."""
TOOLTIP_MIN_CHILD_WEIGHT = """Define el peso mínimo (suma de pesos de las instancias) necesario para seguir 
                            dividiendo un nodo. Un valor de 0.8 ayuda a controlar el sobreajuste, 
                            evitando divisiones que resultarían en nodos con muy pocas instancias."""
TOOLTIP_N_ESTIMATORS = """Especifica el número de árboles a construir. Un valor de 500 significa que el modelo
                        constará de 500 árboles individuales. Más árboles pueden capturar patrones más complejos,
                        pero también aumentan el riesgo de sobreajuste y el costo computacional."""
TOOLTIO_SUBSAMPLE = """Indica la fracción de la muestra de entrenamiento a utilizar para construir cada árbol.
                        Un valor de 0.5 significa que cada árbol se construye utilizando el 50% de los datos, elegidos aleatoriamente.
                        Esto ayuda a prevenir el sobreajuste y añade más aleatoriedad al proceso."""
TOOLTIP_SCALE_POS_WEIGHT = """Utilizado en conjuntos de datos desbalanceados, este parámetro escala
                            el peso de las clases positivas. Un valor de 1 significa que no se aplica ninguna escala,
                            ideal para conjuntos de datos equilibrados o cuando no se desea priorizar
                            una clase sobre otra."""
TOOLTIP_TEST_SIZE = """El 'test size' (tamaño de la prueba) en el contexto de la división de datos en aprendizaje
                    automático, especifica la proporción del conjunto de datos que se separará para el conjunto de prueba.
                    Por ejemplo, un test size de 0.2 significa que el 20% de los datos se usan para probar el modelo, 
                    mientras que el resto se utiliza para entrenarlo. Esta división ayuda a evaluar la eficacia del modelo
                    en datos no vistos, proporcionando una estimación de su rendimiento en escenarios reales.
                    Un tamaño adecuado equilibra entre tener suficientes datos para entrenar el modelo 
                    y suficientes para probarlo de manera efectiva."""
TOOLTIP_SEED = """En el contexto del aprendizaje automático, "seed" o "semilla" se refiere al valor 
                inicial utilizado para inicializar el generador de números aleatorios. Este valor es crucial
                para garantizar la reproducibilidad de los experimentos. Al establecer una semilla específica,
                aseguras que cualquier operación basada en la aleatoriedad (como dividir un conjunto de datos
                en entrenamiento y prueba, inicializar los pesos de un modelo, etc.) produzca los mismos 
                resultados cada vez que se ejecuta el código. Esto es vital para la comparación de modelos,
                la depuración y la publicación de resultados consistentes y reproducibles en el 
                aprendizaje automático."""
