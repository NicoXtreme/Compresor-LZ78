# Utilidad: Manejo del formato personalizado .lz78

import struct
import os

LZ78_SIGNATURE = b"LZ78"
LZ78_VERSION = 1


# ===========================================================
# 📌 GUARDAR ARCHIVO .lz78 (SOLO CÓDIGOS, RECONSTRUIR DICCIONARIO)
# ===========================================================
def save_compressed(file_path: str, codes: list, dictionary: dict, original_size: int):
    """
    Guarda SOLO los códigos (no el diccionario completo).
    
    El diccionario se reconstruye durante la descompresión.
    
    Estructura:
    - Header (8 bytes):
        - Firma: "LZ78" (4 bytes)
        - Versión: 1 (2 bytes)
        - Tamaño original: (2 bytes)
    - Códigos:
        - Número de códigos (4 bytes)
        - Para cada código:
            - Índice (2 bytes)
            - Carácter (1 byte UTF-8)

    Retorna:
        (success: bool, error_msg: str)
    """
    try:
        with open(file_path, "wb") as f:
            # ===== HEADER =====
            f.write(LZ78_SIGNATURE)  # 4 bytes
            f.write(struct.pack(">H", LZ78_VERSION))  # 2 bytes
            f.write(struct.pack(">H", min(original_size, 65535)))  # 2 bytes
            
            # ===== CÓDIGOS ÚNICAMENTE =====
            f.write(struct.pack(">I", len(codes)))  # 4 bytes (número de códigos)
            
            for idx, char in codes:
                f.write(struct.pack(">H", idx))  # 2 bytes (índice)
                
                # Codificar carácter de forma compacta
                if not char:
                    # Carácter vacío
                    f.write(b'\x00')  # 1 byte: 0x00
                elif len(char) == 1 and ord(char) < 128:
                    # ASCII puro: 1 byte
                    f.write(bytes([ord(char)]))
                else:
                    # Extendido: marca + longitud + bytes
                    char_bytes = char.encode('utf-8')
                    f.write(b'\xFF')  # Marca de carácter extendido
                    f.write(struct.pack(">B", len(char_bytes)))  # Longitud
                    f.write(char_bytes)  # Contenido
        
        return True, ""

    except Exception as e:
        return False, f"Error al guardar el archivo: {str(e)}"


# ===========================================================
# 📌 CARGAR ARCHIVO .lz78
# ===========================================================
def load_compressed(file_path: str):
    """
    Carga un archivo .lz78 y retorna:
        (success, codes, dictionary, original_size, error_msg)
    
    El diccionario se reconstruye a partir de los códigos.
    """
    if not os.path.exists(file_path):
        return False, [], {}, 0, "Archivo no encontrado"

    try:
        with open(file_path, "rb") as f:
            # ===== HEADER =====
            signature = f.read(4)
            if signature != LZ78_SIGNATURE:
                return False, [], {}, 0, "Formato incorrecto"
            
            version_bytes = f.read(2)
            version = struct.unpack(">H", version_bytes)[0]
            if version != LZ78_VERSION:
                return False, [], {}, 0, "Versión no soportada"
            
            original_size_bytes = f.read(2)
            original_size = struct.unpack(">H", original_size_bytes)[0]
            
            # ===== CÓDIGOS =====
            codes_count_bytes = f.read(4)
            codes_count = struct.unpack(">I", codes_count_bytes)[0]
            
            codes = []
            dictionary = {}
            next_dict_idx = 1
            
            for _ in range(codes_count):
                idx_bytes = f.read(2)
                idx = struct.unpack(">H", idx_bytes)[0]
                
                # Decodificar carácter
                first_byte = f.read(1)
                if not first_byte:
                    break
                
                byte_val = first_byte[0]
                
                if byte_val == 0x00:
                    # Carácter vacío
                    char = ""
                elif byte_val == 0xFF:
                    # Carácter extendido
                    char_len_bytes = f.read(1)
                    char_len = struct.unpack(">B", char_len_bytes)[0]
                    char_bytes = f.read(char_len)
                    char = char_bytes.decode('utf-8', errors='ignore')
                else:
                    # ASCII simple
                    char = chr(byte_val)
                
                codes.append((idx, char))
                
                # RECONSTRUIR DICCIONARIO DURANTE CARGA
                if idx == 0:
                    new_seq = char
                else:
                    prev_seq = dictionary.get(idx, "")
                    new_seq = prev_seq + char
                
                if next_dict_idx <= 4096:
                    dictionary[next_dict_idx] = new_seq
                    next_dict_idx += 1
            
            return True, codes, dictionary, original_size, ""

    except Exception as e:
        return False, [], {}, 0, f"Archivo corrupto o ilegible: {str(e)}"


# ===========================================================
# 📌 VALIDAR ARCHIVO .lz78
# ===========================================================
def is_valid_lz78_file(file_path: str) -> bool:
    """
    Verifica si un archivo es válido .lz78 revisando el header.
    """
    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, "rb") as f:
            signature = f.read(4)
            return signature == LZ78_SIGNATURE
    except:
        return False
