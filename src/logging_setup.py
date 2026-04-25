import logging
import sys
from config import LOG_FILE

def setup_logging():
    """Настраивает логирование (безопасно — только один раз)"""
    root = logging.getLogger()
    
    # Уже настроено — выходим
    if root.handlers:
        return
    
    root.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    
    root.addHandler(file_handler)
    root.addHandler(stream_handler)

def get_logger(name: str) -> logging.Logger:
    """Возвращает логгер с указанным именем"""
    return logging.getLogger(name)