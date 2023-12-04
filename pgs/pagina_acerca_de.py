import streamlit as st


def pagina_acerca_de(logged: bool) -> None:
    # Mostramos la URL de ToMakeUp
    st.subheader("Acerca de")

    url = "https://tomakeup.es/"

    # Mostrar el texto con el enlace sin subrayado
    st.markdown(
        f"""
        Esta aplicación ha sido desarrollada por <a href="{url}" style="text-decoration: none; color: red;">ToMakeUp</a> para la predicción de la viscosidad en el proceso de fabricación de tintes de cabello. 
        Nuestro sistema utiliza tecnología punta para garantizar la calidad y consistencia de los tintes producidos.         
        """,
        unsafe_allow_html=True,
    )
