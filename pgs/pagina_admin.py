import os
import streamlit as st

from util import download_link
from logger_config import logger


# ----------------------------------------------------------------------------------------------------------------------
def pagina_admin() -> None:
    """
    Despliega la página de administración en la aplicación Streamlit.

    Esta página proporciona funcionalidades de administración para la aplicación, incluyendo la visualización
    de archivos de log y la opción de restaurar los datos de entrenamiento y el modelo de predicción.

    Utiliza dos funciones auxiliares:
    - `show_log_files`: Para mostrar los archivos de log.
    - `reset_model_data`: Para proporcionar una opción de restaurar (borrar) los datos del modelo.

    No se reciben parámetros y no se retorna ningún valor. La función solo afecta la interfaz de usuario
    de la aplicación Streamlit.
    """
    st.subheader("Página de administración", divider="red")

    if not st.session_state["logged"]:
        st.warning("Inicia sesión para acceder a la predicción")
        return

    show_log_files()
    reset_model_data()


# ----------------------------------------------------------------------------------------------------------------------
def show_log_files() -> None:
    """
    Muestra los archivos de log en la página de administración.

    Esta función busca en la carpeta 'logs' todos los archivos con extensión '.log' y los presenta
    en la interfaz de usuario con un enlace para su descarga. En caso de no encontrar archivos de log,
    muestra un mensaje informativo.

    No se reciben parámetros y no se retorna ningún valor. La función solo afecta la interfaz de usuario
    de la aplicación Streamlit.
    """
    # Miro los archivos de log que hay en la carpeta logs y los muestro en la página con un botón de descarga
    st.markdown(
        """
        ##### Logs de la aplicación
        """
    )

    logs = os.listdir("logs")

    if not logs:
        st.info("No hay logs disponibles")
        return

    logs = [log for log in logs if log.endswith(".log")]

    for log in logs:
        download_link(f"logs/{log}", "")


# ----------------------------------------------------------------------------------------------------------------------
def reset_model_data() -> None:
    """
    Proporciona una funcionalidad para restaurar (borrar) los datos de entrenamiento y el modelo de predicción.

    Esta función muestra un botón en la interfaz de usuario que, al ser presionado, intenta borrar los datos
    en las carpetas 'user_data' y 'tmp'. Si la operación es exitosa, muestra un mensaje de éxito; en caso de error,
    muestra un mensaje de error y registra el error en el log.

    No se reciben parámetros y no se retorna ningún valor. La función solo afecta la interfaz de usuario
    de la aplicación Streamlit y realiza operaciones de sistema para borrar archivos.
    """
    # Borro los datos de los modelos
    st.markdown(
        """
        ##### Restaurar datos de entrenamiento y modelo de predicción
        """
    )

    if st.button("Restaurar"):
        try:
            # Borro los datos que haya en la carpeta user_data
            os.system("rm -rf user_data/*")
            # Borro los datos de la carpeta tmp
            os.system("rm -rf tmp/*")
        except Exception as e:
            st.error(f"Error al borrar los datos: {e}")
            logger.error(f"Error al borrar los datos: {e}")
        else:
            st.success("Datos borrados correctamente")
