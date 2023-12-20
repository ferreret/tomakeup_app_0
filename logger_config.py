import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler


# ----------------------------------------------------------------------------------------------------------------------
# Logger configuration
# ----------------------------------------------------------------------------------------------------------------------
def setup_logger():
    """
    Configura y retorna un logger para la aplicación.

    Esta función establece un logger con el nombre 'tomakeup_logger'. El nivel de registro se configura en DEBUG,
    lo que significa que capturará todos los niveles de mensajes (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Pasos de la configuración:
    - Se crea un directorio 'logs' si no existe, para almacenar los archivos de registro.
    - Se configura un manejador de archivos con rotación diaria, que mantiene los registros de los últimos 7 días.
    - Se establece un formato para los mensajes de registro.
    - Si la función se ejecuta más de una vez, se elimina el manejador de archivos anterior para evitar duplicaciones.

    Return:
    - logger: El objeto logger configurado, listo para ser utilizado en la aplicación.

    Ejemplo de Uso:
    >>> logger = setup_logger()
    >>> logger.info("Mensaje de información")
    """
    logger = logging.getLogger("tomakeup_logger")
    logger.setLevel(logging.DEBUG)  

    # Creamos un directorio para los archivos de registro si no existe
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)

    # Configuramos el manejador de archivos
    log_filename = os.path.join(log_directory, time.strftime("%Y-%m-%d") + ".log")
    handler = TimedRotatingFileHandler(
        filename=log_filename,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        delay=False,
        utc=False,
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Eliminamos los manejadores anteriores si se ejecuta setup_logger() más de una vez
    if len(logger.handlers) > 1:
        logger.handlers.pop(0)

    return logger


# ----------------------------------------------------------------------------------------------------------------------
logger = setup_logger()
