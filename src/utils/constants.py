# Utilidad: Constantes globales de la aplicación

# ============================================================
# 📌 Extensiones válidas
# ============================================================

VALID_TEXT_EXTENSIONS = ['.txt']
VALID_COMPRESSED_EXTENSIONS = ['.lz78']


# ============================================================
# 📌 Límites del sistema
# ============================================================

MAX_FILE_SIZE = 10 * 1024 * 1024   # 10 MB
MAX_DICTIONARY_SIZE = 4096
MIN_FILE_SIZE = 1  # 1 byte mínimo permitido


# ============================================================
# 📌 Formato .lz78
# ============================================================

LZ78_FORMAT_VERSION = 1
LZ78_HEADER_SIZE = 8
LZ78_SIGNATURE = b'LZ78'   # Firma en 4 bytes


# ============================================================
# 📌 Encoding por defecto
# ============================================================

DEFAULT_ENCODING = 'utf-8'
