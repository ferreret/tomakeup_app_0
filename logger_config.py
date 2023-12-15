import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler


# ----------------------------------------------------------------------------------------------------------------------
# Logger configuration
# ----------------------------------------------------------------------------------------------------------------------
def setup_logger():
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

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Eliminamos los manejadores anteriores si se ejecuta setup_logger() más de una vez
    if len(logger.handlers) > 1:
        logger.handlers.pop(0)

    return logger


# ----------------------------------------------------------------------------------------------------------------------
logger = setup_logger()