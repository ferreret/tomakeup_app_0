import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

from pgs.pagina_inicio import pagina_inicio
from pgs.pagina_prediccion import pagina_prediccion
import yaml
from yaml.loader import SafeLoader

HTML_BANNER = """
    <div style="background-color:red;padding:10px;border-radius:10px;margin-bottom:30px;">
    <h1 style="color:white;text-align:center;">ToMakeUp</h1>
    </div>
    """


def load_auth_yaml():
    with open("auth.yaml") as f:
        return yaml.load(f, Loader=SafeLoader)


def main() -> None:
    config_app()
    st.markdown(
        HTML_BANNER,
        unsafe_allow_html=True,
    )

    create_menu()


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


def create_menu() -> None:
    with st.sidebar:
        selected_page = option_menu(
            "ToMakeUp",
            ["Inicio", "Predición", "Entrenamiento", "Acerca de"],
            menu_icon="hamburger",
            default_index=0,
        )

        config = load_auth_yaml()

        authenticator = stauth.Authenticate(
            config["credentials"],
            config["cookie"]["name"],
            config["cookie"]["key"],
            config["cookie"]["expiry_days"],
            config["preauthorized"],
        )

        authenticator.login("Inicio de sesión")

        logged = False

        if st.session_state["authentication_status"]:
            authenticator.logout("Logout", "main", key="unique_key")
            logged = True
            st.write(f'Bienvenido *{st.session_state["name"]}*')
        elif st.session_state["authentication_status"] is False:
            st.error("Username/password no es correcto")
        elif st.session_state["authentication_status"] is None:
            st.warning("Introducte tus credenciales")

    if selected_page == "Inicio":
        pagina_inicio(logged)
    elif selected_page == "Predición":
        pagina_prediccion(logged)
    elif selected_page == "Entrenamiento":
        pass
    elif selected_page == "Acerca de":
        pass


if __name__ == "__main__":
    # hashed_passwords = stauth.Hasher(["nicolas", "guillermo", "lakme"]).generate()
    # print(hashed_passwords)
    main()
