# Utilidad: Manejo del formato personalizado .lz78

import json
import os

LZ78_SIGNATURE = "LZ78"
LZ78_VERSION = 1


# ===========================================================
# 📌 GUARDAR ARCHIVO .lz78
# ===========================================================
def save_compressed(file_path: str, codes: list, dictionary: dict, original_size: int):
    """
    Guarda la información comprimida en un archivo .lz78
    usando un formato JSON estructurado.

    Retorna:
        (success: bool, error_msg: str)
    """
    try:
        data = {
            "header": {
                "signature": LZ78_SIGNATURE,
                "version": LZ78_VERSION,
                "original_size": original_size
            },
            "dictionary": [
                {
                    "index": idx,
                    "sequence": seq
                }
                for idx, seq in dictionary.items()
            ],
            "codes": [
                {"idx": idx, "char": ch}
                for idx, ch in codes
            ]
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

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
    """
    if not os.path.exists(file_path):
        return False, [], {}, 0, "Archivo no encontrado"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    except Exception:
        return False, [], {}, 0, "Archivo corrupto o ilegible"

    # ----------------------------
    # VALIDAR HEADER
    # ----------------------------
    header = data.get("header", {})

    if header.get("signature") != LZ78_SIGNATURE:
        return False, [], {}, 0, "Formato incorrecto"

    if header.get("version") != LZ78_VERSION:
        return False, [], {}, 0, "Versión no soportada"

    original_size = header.get("original_size", 0)

    # ----------------------------
    # CARGAR DICCIONARIO
    # ----------------------------
    raw_dict = data.get("dictionary", [])
    dictionary = {}

    try:
        for entry in raw_dict:
            dictionary[int(entry["index"])] = entry["sequence"]
    except:
        return False, [], {}, 0, "Diccionario corrupto"

    # ----------------------------
    # CARGAR CÓDIGOS
    # ----------------------------
    raw_codes = data.get("codes", [])
    codes = []

    try:
        for c in raw_codes:
            codes.append((int(c["idx"]), c["char"]))
    except:
        return False, [], {}, 0, "Códigos corruptos"

    return True, codes, dictionary, original_size, ""


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
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        header = data.get("header", {})
        return header.get("signature") == LZ78_SIGNATURE

    except:
        return False
