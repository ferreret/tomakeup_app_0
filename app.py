import streamlit as st
import streamlit_authenticator as stauth  # type: ignore
import yaml  # type: ignore
from streamlit_option_menu import option_menu  # type: ignore
from yaml.loader import SafeLoader  # type: ignore

from constants import HTML_BANNER
from pgs.pagina_acerca_de import pagina_acerca_de
from pgs.pagina_admin import pagina_admin
from pgs.pagina_eda import pagina_eda
from pgs.pagina_entrenamiento import pagina_entrenamiento
from pgs.pagina_inicio import pagina_inicio
from pgs.pagina_prediccion import pagina_prediccion
from logger_config import logger


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
    # Hago un control de excepciones general para que la aplicación no se caiga
    try:
        create_menu()
    except Exception as e:
        logger.error(e)
        st.error(
            "¡Algo ha fallado! :sweat_smile: Por favor, reinicia la aplicación y vuelve a intentarlo."
        )
        st.error(e)
        st.stop()


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

    authenticator.login(
        fields={
            "Form name": "Inicio de sesión",
            "Username": "Nombre de usuario",
            "Password": "Contraseña",
            "Login": "Iniciar sesión",
        }
    )

    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "main", key="unique_key")
        st.write(f'Bienvenido *{st.session_state["name"]}*')
        return True
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password no es correcto")
    elif st.session_state["authentication_status"] is None:
        st.warning("Introduce tus credenciales")
        st.info("Utiliza 'test / test' para probar la aplicación")

    return False


# ----------------------------------------------------------------------------------------------------------------------
def create_sidebar_menu() -> str:
    """
    Crea un menú lateral en la aplicación Streamlit y devuelve la página seleccionada por el usuario.

    Returns:
        str: Nombre de la página seleccionada por el usuario.
    """

    # Inicializamos la variable logged en caso de que no exista
    if "logged" not in st.session_state:
        st.session_state["logged"] = False

    with st.sidebar:
        # En el caso de que el usuario sea un administrador, añado la página de administración
        # if (
        #     st.session_state["logged"]
        #     and st.session_state["username"] in load_auth_yaml()["admins"]
        # ):
        selected_page = option_menu(
            "Menú",
            [
                "Inicio",
                "EDA",
                "Predición",
                "Entrenamiento",
                "Admin",
                "Acerca de",
            ],
            menu_icon="hamburger",
            default_index=0,
        )
        # else:
        #     selected_page = option_menu(
        #         "Menú",
        #         ["Inicio", "EDA", "Predición", "Entrenamiento", "Acerca de"],
        #         menu_icon="hamburger",
        #         default_index=0,
        #     )

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
        "Entrenamiento": pagina_entrenamiento,
        "Acerca de": pagina_acerca_de,
        "Admin": pagina_admin,
    }

    selected_page = create_sidebar_menu()

    if selected_page in page_functions:
        page_functions[selected_page]()


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # hashed_passwords = stauth.Hasher(
    #     [
    #         "nicolas",
    #         "test",
    #     ]
    # ).generate()
    # print(hashed_passwords)
    main()
