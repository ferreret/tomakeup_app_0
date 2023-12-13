import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_option_menu import option_menu
from yaml.loader import SafeLoader
from constants import HTML_BANNER

from pgs.pagina_acerca_de import pagina_acerca_de
from pgs.pagina_eda import pagina_eda
from pgs.pagina_inicio import pagina_inicio
from pgs.pagina_prediccion import pagina_prediccion


# ----------------------------------------------------------------------------------------------------------------------
def load_auth_yaml() -> dict:
    with open("auth.yaml") as f:
        return yaml.load(f, Loader=SafeLoader)


# ----------------------------------------------------------------------------------------------------------------------
def main() -> None:
    config_app()
    st.markdown(
        HTML_BANNER,
        unsafe_allow_html=True,
    )
    create_menu()


# ----------------------------------------------------------------------------------------------------------------------
def config_app() -> None:
    """
    Configures the ToMakeUp app with Streamlit's `set_page_config` function.

    Sets the page title to "ToMakeUp", the page icon to ":haircut:", the layout to "wide",
    and the initial sidebar state to "expanded".
    """
    st.set_page_config(
        page_title="ToMakeUp",
        page_icon=":haircut:",
        layout="wide",
        initial_sidebar_state="expanded",
    )


# ----------------------------------------------------------------------------------------------------------------------
def handle_authentication() -> bool:
    """
    Maneja el proceso de autenticación del usuario.

    Returns:
        bool: Estado de autenticación del usuario (True si está autenticado, False en caso contrario).
    """
    config = load_auth_yaml()
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )

    authenticator.login("Inicio de sesión")

    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "main", key="unique_key")
        st.write(f'Bienvenido *{st.session_state["name"]}*')
        return True
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password no es correcto")
    elif st.session_state["authentication_status"] is None:
        st.warning("Introduce tus credenciales")

    return False


# ----------------------------------------------------------------------------------------------------------------------
def create_sidebar_menu() -> str:
    """
    Crea un menú lateral en la aplicación Streamlit y devuelve la página seleccionada por el usuario.

    Returns:
        str: Nombre de la página seleccionada por el usuario.
    """
    with st.sidebar:
        selected_page = option_menu(
            "Menú",
            ["Inicio", "EDA", "Predición", "Entrenamiento", "Acerca de"],
            menu_icon="hamburger",
            default_index=0,
        )
        st.session_state["logged"] = handle_authentication()
        return selected_page


# ----------------------------------------------------------------------------------------------------------------------
def create_menu() -> None:
    """
    Crea un menú lateral en una aplicación Streamlit y gestiona la navegación entre diferentes páginas.
    """

    # Diccionario para mapear nombres de páginas a funciones
    page_functions = {
        "Inicio": pagina_inicio,
        "EDA": pagina_eda,
        "Predición": pagina_prediccion,
        "Acerca de": pagina_acerca_de,
    }

    selected_page = create_sidebar_menu()

    if selected_page in page_functions:
        page_functions[selected_page]()


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # hashed_passwords = stauth.Hasher(["nicolas", "guillermo", "lakme"]).generate()
    # print(hashed_passwords)
    main()
