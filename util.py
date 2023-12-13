import base64

import streamlit as st


# ----------------------------------------------------------------------------------------------------------------------
def get_binary_file_downloader_html(bin_file, file_label="File") -> str:
    """
    Genera un enlace HTML para descargar un archivo binario.

    Args:
        bin_file (str): Ruta al archivo binario que se quiere descargar.
        file_label (str, opcional): Etiqueta para el archivo en el enlace de descarga. Por defecto es "File".

    Returns:
        str: Una cadena de caracteres que representa un enlace de descarga HTML.
    """

    # Abre el archivo binario en modo de lectura binaria
    with open(bin_file, "rb") as f:
        data = f.read()  # Lee los datos del archivo

    # Codifica los datos binarios a una cadena base64
    bin_str = base64.b64encode(data).decode()

    # Crea un enlace HTML para la descarga.
    # 'data:application/octet-stream' indica que es un stream de datos binarios.
    # 'base64,{bin_str}' es el archivo codificado en base64.
    # 'download="{bin_file}"' sugiere el nombre del archivo para la descarga.
    # 'style="text-decoration: none;"' elimina el subrayado del enlace para mejorar la estética.
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}" style="text-decoration: none;">Descargar {file_label}</a>'

    return href  # Devuelve el enlace de descarga


# ----------------------------------------------------------------------------------------------------------------------
def download_link(file_path: str, description: str) -> None:
    """
    Muestra un enlace de descarga para un archivo dado y una descripción.

    Args:
        file_path (str): Ruta del archivo a descargar.
        description (str): Descripción del archivo.
    """
    file_name = file_path.split("/")[-1]
    st.markdown(
        get_binary_file_downloader_html(file_path, file_name), unsafe_allow_html=True
    )
    st.write(description)
