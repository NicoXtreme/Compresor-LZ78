# Modelo: Manejo de archivos (lectura, escritura, validación)

import os

class FileHandler:
    def __init__(self):
        self.current_file = None
        self.content = ""
        self.file_encoding = "utf-8"

    # -----------------------------------------
    # 📌 LEER ARCHIVO
    # -----------------------------------------
    def read_file(self, path: str):
        """
        Lee un archivo de texto con validaciones estrictas.

        Retorna:
            (success: bool, content: str, error_msg: str)
        """
        self.current_file = path

        # Validar existencia
        if not os.path.exists(path):
            return False, "", "Archivo no encontrado"

        # Validar que sea archivo regular
        if not os.path.isfile(path):
            return False, "", "Ruta inválida"

        try:
            with open(path, "r", encoding=self.file_encoding) as f:
                content = f.read()
        except:
            return False, "", "Error al leer el archivo"

        # Validar vacío
        if not content.strip():
            return False, "", "Archivo vacío"

        self.content = content
        return True, content, ""

    # -----------------------------------------
    # 📌 ESCRIBIR ARCHIVO
    # -----------------------------------------
    def write_file(self, path: str, content: str):
        """
        Escribe contenido en un archivo.

        Retorna:
            (success: bool, error_msg: str)
        """
        if not path or not isinstance(path, str):
            return False, "Ruta inválida"

        try:
            with open(path, "w", encoding=self.file_encoding) as f:
                f.write(content)
        except:
            return False, "Error al escribir el archivo"

        return True, ""

    # -----------------------------------------
    # 📌 VALIDAR ARCHIVO
    # -----------------------------------------
    def validate_file(self, path: str):
        """
        Verifica si un archivo existe, es legible y no está vacío.

        Retorna:
            (is_valid: bool, error_msg: str)
        """
        if not os.path.exists(path):
            return False, "Archivo no encontrado"

        if not os.path.isfile(path):
            return False, "Ruta inválida"

        try:
            size = os.path.getsize(path)
            if size == 0:
                return False, "Archivo vacío"
        except:
            return False, "Error al leer el archivo"

        return True, ""
