import streamlit as st
from constants import APP_DESCRIPTION, FEAUTURES_DESCRIPTION, FILES_TO_DOWNLOAD

from util import download_link


def pagina_inicio() -> None:
    """
    Muestra la página de inicio de la aplicación Streamlit.
    """
    st.image("images/portada.png", use_column_width=True)

    st.markdown(APP_DESCRIPTION)

    st.write("")


    if not st.session_state["logged"]:
        st.warning(
            """
            #### Inicia sesión para acceder a las funcionalidades
            """
        )
        return

    st.markdown(
        """
        ### Archivos de la aplicación
        """
    )

    for file in FILES_TO_DOWNLOAD:
        download_link(file["ruta"], file["descripcion"])
        st.markdown("---")

    st.markdown(FEAUTURES_DESCRIPTION)
