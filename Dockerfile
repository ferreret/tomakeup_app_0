# Usa una imagen base oficial de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu aplicación al contenedor
COPY . .

# El puerto en el que se ejecutará la aplicación
EXPOSE 8501

# El comando para ejecutar tu aplicación Streamlit
CMD ["streamlit", "run", "app.py"]
