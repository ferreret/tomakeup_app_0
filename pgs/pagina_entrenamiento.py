import os
import shutil
import joblib

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt
from sklearn.metrics import auc, classification_report, confusion_matrix, roc_curve
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from constants import (
    ARCHIVO_DATOS_ENTRENAMIENTO_USUARIO,
    CAPACIDAD_REACTORES,
    RUTA_DATOS_ENTRENAMIENTO_USUARIO,
    RUTA_MODELO_USUARIO,
    TEMP_FOLDER,
    TOOLTIO_SUBSAMPLE,
    TOOLTIP_ALPHA,
    TOOLTIP_COLSAMPLE_BYTREE,
    TOOLTIP_GAMMA,
    TOOLTIP_LEARNING_RATE,
    TOOLTIP_MAX_DEPTH,
    TOOLTIP_MIN_CHILD_WEIGHT,
    TOOLTIP_N_ESTIMATORS,
    TOOLTIP_SCALE_POS_WEIGHT,
    TOOLTIP_SEED,
    TOOLTIP_TEST_SIZE,
    USUARIO_FOLDER,
)
from data_repo import read_data
from logger_config import logger


# ----------------------------------------------------------------------------------------------------------------------
def pagina_entrenamiento() -> None:
    """
    Presenta una interfaz de usuario en Streamlit para el entrenamiento de un modelo predictivo utilizando XGBoost.

    Esta función permite al usuario cargar un archivo CSV para entrenar el modelo, ajustar parámetros de entrenamiento
    y ejecutar el proceso de entrenamiento. También ofrece la opción de predeterminar los datos y el modelo
    después del entrenamiento.

    La interfaz incluye:
    - Un cargador de archivos para el fichero de entrenamiento.
    - Entradas para ajustar varios parámetros del modelo XGBoost.
    - Un botón para iniciar el entrenamiento del modelo.
    - La opción de predeterminar los resultados del entrenamiento.

    No se reciben parámetros y no se retorna ningún valor. La función afecta la interfaz de usuario
    de la aplicación Streamlit y puede desencadenar el entrenamiento del modelo.
    """
    st.subheader("Entrenamiento modelo predictivo, (XGBoost)", divider="red")

    if not st.session_state["logged"]:
        st.warning("Inicia sesión para acceder a la predicción")
        return

    training_file = st.file_uploader(
        "Sube el fichero de entrenamiento", type=["csv"], accept_multiple_files=False
    )

    st.markdown("**Parámetros de entrenamiento**")

    # Creo 3 columnas para mostrar los datos de entrenamiento
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        alpha = st.number_input("alpha", value=0.5, step=0.1, help=TOOLTIP_ALPHA)
        max_depth = st.number_input(
            "max_depth", value=4, step=1, help=TOOLTIP_MAX_DEPTH
        )
        scale_pos_weight = st.number_input(
            "scale_pos_weight", value=1.0, step=0.1, help=TOOLTIP_SCALE_POS_WEIGHT
        )

    with col2:
        colsample_bytree = st.number_input(
            "colsample_bytree", value=0.9, step=0.1, help=TOOLTIP_COLSAMPLE_BYTREE
        )
        min_child_weight = st.number_input(
            "min_child_weight", value=0.8, step=0.1, help=TOOLTIP_MIN_CHILD_WEIGHT
        )
        test_size = st.number_input(
            "test_size", value=0.3, step=0.1, help=TOOLTIP_TEST_SIZE
        )

    with col3:
        gamma = st.number_input("gamma", value=0.2, step=0.1, help=TOOLTIP_GAMMA)
        n_estimators = st.number_input(
            "n_estimators", value=500, step=10, help=TOOLTIP_N_ESTIMATORS
        )
        seed = st.number_input("seed", value=0, step=1, help=TOOLTIP_SEED)

    with col4:
        learning_rate = st.number_input(
            "learning_rate", value=0.005, step=0.001, help=TOOLTIP_LEARNING_RATE
        )
        subsample = st.number_input(
            "subsample", value=0.5, step=0.1, help=TOOLTIO_SUBSAMPLE
        )

    predeterminar = st.checkbox(
        """Predeterminar datos y modelo. (Solo marcar en el caso de que previamente se haya entrenado
        y los resultados sean satisfactorios )"""
    )

    if st.button("Entrenar modelo"):
        if training_file is not None:
            try:
                ruta_fichero = save_training_data(training_file)
                train_data(
                    alpha=alpha,
                    colsample_bytree=colsample_bytree,
                    gamma=gamma,
                    learning_rate=learning_rate,
                    max_depth=max_depth,
                    min_child_weight=min_child_weight,
                    n_estimators=n_estimators,
                    scale_pos_weight=scale_pos_weight,
                    seed=seed,
                    subsample=subsample,
                    test_size=test_size,
                    training_file=ruta_fichero,
                    predeterminar=predeterminar,
                )
            except Exception as e:
                logger.error(e)
                st.error(f"Error: {e}")
        else:
            st.error("Por favor, sube un fichero de entrenamiento")


# ----------------------------------------------------------------------------------------------------------------------
def save_training_data(training_file: str) -> str:
    """
    Guarda un archivo de entrenamiento en una carpeta temporal.

    Esta función realiza varias tareas para manejar el almacenamiento de un archivo de entrenamiento.
    Se asume que 'training_file' es un objeto de tipo archivo (como el retornado por 'st.file_uploader' en Streamlit).

    Parámetros:
    - training_file: str
        El archivo de entrenamiento a guardar. Debe ser un objeto de archivo con un método 'getbuffer'.

    Return:
    - str
        Ruta del archivo de entrenamiento guardado.

    Funcionamiento:
    1. Verificación y manejo de la carpeta temporal:
        - Se comprueba si existe una carpeta llamada "tmp" (temp_folder).
        - Si la carpeta existe, se elimina junto con todo su contenido.
        - Se crea una nueva carpeta "tmp", asegurando su existencia.

    2. Guardado del archivo de entrenamiento:
        - El archivo de entrenamiento se guarda en la carpeta "tmp" con el nombre "training.csv".
        - Se utiliza 'os.path.join' para asegurar la correcta formación del path del archivo.
        - Se abre el archivo en modo de escritura binaria ('wb').
        - Se escribe el contenido del 'training_file' en el nuevo archivo usando 'getbuffer'.
    """

    # Comprobamos que existe la carpeta temporal, si no existe la creamos
    # Si existe, borramos su contenido

    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    os.makedirs(TEMP_FOLDER, exist_ok=True)

    # Guardamos el fichero de entrenamiento en la carpeta temporal y le cambiamos el nombre a "training.csv"
    ruta_fichero = os.path.join(TEMP_FOLDER, ARCHIVO_DATOS_ENTRENAMIENTO_USUARIO)
    with open(ruta_fichero, "wb") as f:
        f.write(training_file.getbuffer())

    return ruta_fichero


# ----------------------------------------------------------------------------------------------------------------------
def train_data(
    alpha: float,
    colsample_bytree: float,
    gamma: float,
    learning_rate: float,
    max_depth: int,
    min_child_weight: float,
    n_estimators: int,
    scale_pos_weight: float,
    seed: int,
    subsample: float,
    test_size: float,
    training_file: str,
    predeterminar: bool,
) -> None:
    """
    Entrena un modelo de clasificación usando XGBoost con los datos y parámetros proporcionados.

    Parámetros:
    - alpha, colsample_bytree, gamma, learning_rate, max_depth, min_child_weight,
    n_estimators, scale_pos_weight, seed, subsample, test_size: Parámetros del modelo XGBoost.
    - training_file: Ruta al archivo CSV que contiene los datos de entrenamiento.
    - predeterminar: Bool que indica si se debe predeterminar el modelo y los datos después del entrenamiento.

    La función procesa los datos de entrenamiento, entrena el modelo de XGBoost con los parámetros especificados,
    y muestra los resultados del entrenamiento en la interfaz de usuario de Streamlit. Si 'predeterminar' es True,
    guarda el modelo y los datos de entrenamiento para uso futuro.

    No se retorna ningún valor.
    """
    # Creo un spinner para mostrar que se está entrenando el modelo
    with st.spinner("Entrenando modelo, por favor, espera..."):
        training_data_df = pd.read_csv(training_file)
        training_data_df["capacidad_reactor"] = training_data_df["reactor"].map(
            CAPACIDAD_REACTORES
        )
        training_data_df["grado_llenado"] = (
            (training_data_df["cantidad"] / training_data_df["capacidad_reactor"]) * 100
        ).round(2)
        components_df = read_data("componentes.csv")
        training_data_df = pd.merge(
            training_data_df,
            components_df,
            left_on="matcode",
            right_on="material",
            how="left",
        )

        # Elimino las columnas que no se van a utilizar en el entrenamiento
        training_data_df.drop(
            columns=[
                "orden",
                "fecha",
                "matcode",
                "capacidad_reactor",
                "material",
            ],
            inplace=True,
        )

        # Separo los datos de entrenamiento en X e y
        X = training_data_df.drop(columns=["target"])
        y = training_data_df["target"]
        # One-hot encoding para la columna reactor
        X_encoded = pd.get_dummies(X, columns=["reactor"], drop_first=True)
        # Separo los datos en train y test
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y, test_size=test_size, random_state=seed
        )

        xgb_clf = XGBClassifier(
            alpha=alpha,
            colsample_bytree=colsample_bytree,
            gamma=gamma,
            learning_rate=learning_rate,
            max_depth=max_depth,
            min_child_weight=min_child_weight,
            n_estimators=n_estimators,
            scale_pos_weight=scale_pos_weight,
            seed=seed,
            subsample=subsample,
        )

        xgb_clf.fit(X_train, y_train)

        show_trainning_results(xgb_clf, X_train, y_train, X_test, y_test, predeterminar)


# ----------------------------------------------------------------------------------------------------------------------
def show_trainning_results(
    model, X_train, y_train, X_test, y_test, predeterminar: bool
):
    """
    Muestra los resultados del entrenamiento de un modelo en la interfaz de usuario de Streamlit.

    Parámetros:
    - model: El modelo de XGBoost entrenado.
    - X_train, y_train: Datos de entrenamiento y sus etiquetas.
    - X_test, y_test: Datos de prueba y sus etiquetas.
    - predeterminar: Bool que indica si se debe guardar el modelo y los datos de entrenamiento.

    Esta función visualiza el reporte de clasificación, la matriz de confusión y las curvas ROC y AUC.
    Si 'predeterminar' es True, también guarda el modelo y los datos de entrenamiento.

    No se retorna ningún valor.
    """
    y_pred = model.predict(X_test)

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Reporte de clasificación", expanded=True):
            target_names = ["Buena", "Mala"]
            report_df = show_report(y_test, y_pred, target_names)
            st.table(report_df)

    with col2:
        with st.expander("Matriz de confusión", expanded=True):
            show_confusion_matrix(y_test, y_pred)

    with st.expander("Curvas ROC y AUC", expanded=True):
        fig = plot_ROC_AUC_curves(
            model, X_train, y_train, X_test, y_test, model_name="XGBoost"
        )
        st.plotly_chart(fig, use_container_width=True)

    if predeterminar:
        try:
            save_user_data_model(model)
        except Exception as e:
            logger.error(e)
            st.error(f"Error: {e}")
        else:
            st.success("Modelo y datos de entrenamiento predeterminados correctamente")
            st.snow()


# ----------------------------------------------------------------------------------------------------------------------
def save_user_data_model(model):
    """
    Guarda el modelo entrenado y los datos de entrenamiento en una ubicación específica.

    Parámetros:
    - model: El modelo de XGBoost entrenado.

    Esta función guarda el modelo en la carpeta 'user_data' y los datos de entrenamiento en una carpeta temporal.
    Se utilizan las rutas definidas en las constantes del módulo.

    No se retorna ningún valor.
    """
    # El archivo de entrenamiento se guarda en la carpeta "tmp" con el nombre "datos_entrenamiento.csv".
    # lo guardo en la carpeta user_data
    ruta_fichero_tmp = os.path.join(TEMP_FOLDER, ARCHIVO_DATOS_ENTRENAMIENTO_USUARIO)

    # Compruebo si existe la carpeta user_data, si no existe la creo
    if not os.path.exists(USUARIO_FOLDER):
        os.makedirs(USUARIO_FOLDER, exist_ok=True)

    # Si existen los datos de entrenamiento en la carpeta user_data, los borro
    if os.path.exists(RUTA_DATOS_ENTRENAMIENTO_USUARIO):
        os.remove(RUTA_DATOS_ENTRENAMIENTO_USUARIO)
    # Si existe el modelo en la carpeta user_data, lo borro
    if os.path.exists(RUTA_MODELO_USUARIO):
        os.remove(RUTA_MODELO_USUARIO)

    shutil.copyfile(ruta_fichero_tmp, RUTA_DATOS_ENTRENAMIENTO_USUARIO)
    # Guardamos el modelo en la carpeta user_data usando joblib
    joblib.dump(model, RUTA_MODELO_USUARIO)


# ----------------------------------------------------------------------------------------------------------------------
def show_confusion_matrix(y_test, y_pred):
    cm_plot = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm_plot, annot=True, cmap="Reds", fmt="g")
    plt.xlabel("Predicción")
    plt.ylabel("Real")
    labels = ["Buena", "Mala"]
    plt.xticks(ticks=np.arange(len(labels)) + 0.5, labels=labels)
    plt.yticks(ticks=np.arange(len(labels)) + 0.5, labels=labels, rotation=0)
    st.pyplot(plt, use_container_width=True)


# -----------------------------------------------------------------------------------------------------------------------
def show_report(y_test, y_pred, target_names):
    """
    Genera un reporte de clasificación para un modelo de clasificación binaria.
    """
    report = classification_report(
        y_test, y_pred, target_names=target_names, output_dict=True
    )
    report_df = pd.DataFrame(report).transpose()
    report_df = report_df.round(2)

    return report_df


# ----------------------------------------------------------------------------------------------------------------------
def plot_ROC_AUC_curves(model, X_train, y_train, X_test, y_test, model_name):
    """
    Plots the ROC curves and AUC scores using Plotly for the given model,
    using both training and testing data.
    """
    # Get the probabilities of the positive class for training and testing data
    train_probs = model.predict_proba(X_train)[:, 1]
    test_probs = model.predict_proba(X_test)[:, 1]

    # Calculate the ROC curve and AUC for training data
    fpr_train, tpr_train, _ = roc_curve(y_train, train_probs)
    roc_auc_train = auc(fpr_train, tpr_train)

    # Calculate the ROC curve and AUC for test data
    fpr_test, tpr_test, _ = roc_curve(y_test, test_probs)
    roc_auc_test = auc(fpr_test, tpr_test)

    # Create the plot
    fig = go.Figure()

    # Add the ROC curve for the training data
    fig.add_trace(
        go.Scatter(
            x=fpr_train,
            y=tpr_train,
            mode="lines",
            name=f"Train ROC curve (area = {roc_auc_train:.2f})",
            line=dict(color="blue"),
        )
    )

    # Add the ROC curve for the testing data
    fig.add_trace(
        go.Scatter(
            x=fpr_test,
            y=tpr_test,
            mode="lines",
            name=f"Test ROC curve (area = {roc_auc_test:.2f})",
            line=dict(color="red"),
        )
    )

    # Add a gray dashed line representing random guessing
    fig.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Random Guessing",
            line=dict(color="gray", dash="dash"),
        )
    )

    # Set the layout of the plot
    fig.update_layout(
        title=f"Receiver Operating Characteristic (ROC) Curve for {model_name}",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        yaxis=dict(range=[0.0, 1.05]),
        xaxis=dict(range=[0.0, 1.0]),
        legend=dict(x=1, y=0),
        height=600,
    )

    return fig
