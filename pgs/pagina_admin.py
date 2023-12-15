import os
import streamlit as st

from util import download_link


def pagina_admin() -> None:
    st.subheader("Página de administración", divider="red")

    # Miro los archivos de log que hay en la carpeta logs y los muestro en la página con un botón de descarga
    st.markdown(
        """
        ##### Logs de la aplicación
        """
    )

    logs = os.listdir("logs")
    logs = [log for log in logs if log.endswith(".log")]

    for log in logs:
        download_link(f"logs/{log}", "")
