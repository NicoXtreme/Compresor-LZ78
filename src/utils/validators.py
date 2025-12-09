# Utilidad: Validadores de archivos y datos

import os
from src.utils import constants


def is_valid_text_file(path: str) -> bool:
    """
    Verifica que el archivo sea un archivo de texto válido.
    
    Args:
        path: ruta del archivo
    
    Returns:
        True si es válido, False en caso contrario
    """
    if not path:
        return False
    
    if not os.path.exists(path):
        return False
    
    if not os.path.isfile(path):
        return False
    
    # Verificar extensión
    _, ext = os.path.splitext(path)
    if ext.lower() not in constants.VALID_TEXT_EXTENSIONS:
        return False
    
    return True


def is_valid_lz78_file(path: str) -> bool:
    """
    Verifica que el archivo sea un archivo .lz78 válido.
    
    Args:
        path: ruta del archivo
    
    Returns:
        True si es válido, False en caso contrario
    """
    if not path:
        return False
    
    if not os.path.exists(path):
        return False
    
    if not os.path.isfile(path):
        return False
    
    # Verificar extensión
    _, ext = os.path.splitext(path)
    if ext.lower() not in constants.VALID_COMPRESSED_EXTENSIONS:
        return False
    
    # Verificar firma binaria LZ78
    try:
        with open(path, 'rb') as f:
            signature = f.read(4)
            return signature == b"LZ78"
    except:
        return False


def is_empty_file(path: str) -> bool:
    """
    Verifica si un archivo está vacío.
    
    Args:
        path: ruta del archivo
    
    Returns:
        True si está vacío, False si tiene contenido
    """
    if not os.path.exists(path):
        return True
    
    return os.path.getsize(path) == 0


def is_readable_file(path: str) -> bool:
    """
    Verifica si un archivo es legible.
    
    Args:
        path: ruta del archivo
    
    Returns:
        True si es legible, False en caso contrario
    """
    if not os.path.exists(path):
        return False
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            f.read(1)
        return True
    except:
        return False


def validate_file_content(content: str, max_size: int = 10485760) -> tuple:
    """
    Valida el contenido de un archivo.
    
    Args:
        content: contenido del archivo
        max_size: tamaño máximo permitido en bytes (por defecto 10 MB)
    
    Returns:
        (is_valid: bool, error_msg: str)
    """
    # Verificar que no esté vacío
    if not content or not content.strip():
        return False, "Archivo vacío"
    
    # Verificar tamaño
    content_bytes = content.encode('utf-8')
    if len(content_bytes) > max_size:
        return False, f"Archivo demasiado grande (máximo {max_size // (1024*1024)} MB)"
    
    return True, ""
