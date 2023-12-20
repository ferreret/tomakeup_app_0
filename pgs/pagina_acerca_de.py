import streamlit as st


def pagina_acerca_de() -> None:
    """
    Despliega una página de 'Acerca de' en la aplicación Streamlit.

    Esta página proporciona información sobre ToMakeUp, la entidad desarrolladora de la aplicación.
    Se enfoca en explicar brevemente el propósito de la aplicación: la predicción de la viscosidad en la
    fabricación de tintes para el cabello, destacando el uso de tecnología avanzada para garantizar
    calidad y consistencia en los productos.

    La función utiliza el método `st.markdown` de Streamlit para mostrar un texto que incluye un enlace
    a la página web de ToMakeUp. Se personaliza el estilo del enlace para eliminar el subrayado y cambiar
    el color del texto, lo que ayuda a integrar el enlace de manera más armoniosa en el diseño de la página.

    No se reciben parámetros y no se retorna ningún valor. La función solo afecta la interfaz de usuario
    de la aplicación Streamlit.
    # Mostramos la URL de ToMakeUp
    st.subheader("Acerca de")
    """

    url = "https://tomakeup.es/"

    # Mostrar el texto con el enlace sin subrayado
    st.markdown(
        f"""
        Esta aplicación ha sido desarrollada por <a href="{url}" style="text-decoration: none; color: red;">ToMakeUp</a> para la predicción de la viscosidad en el proceso de fabricación de tintes de cabello. 
        Nuestro sistema utiliza tecnología punta para garantizar la calidad y consistencia de los tintes producidos.         
        """,
        unsafe_allow_html=True,
    )
