import base64

import streamlit as st


def get_binary_file_downloader_html(bin_file, file_label="File") -> str:
    with open(bin_file, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    # Agregar estilo CSS inline para quitar el subrayado
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}" style="text-decoration: none;">Descargar {file_label}</a>'
    return href
