# Controlador: Lógica de conexión entre vista y modelo

import os
from src.model.lz78_compressor import LZ78Compressor
from src.model.file_handler import FileHandler
from src.model.statistics import CompressionStatistics
from src.utils import validators, file_format, constants


class MainController:
    """
    Controlador que conecta la vista con el modelo.
    Implementa la lógica de negocio de la aplicación.
    """
    
    def __init__(self, view):
        """
        Inicializa el controlador.
        
        Args:
            view: instancia de MainWindow (la vista)
        """
        self.view = view
        self.compressor = LZ78Compressor(constants.MAX_DICTIONARY_SIZE)
        self.file_handler = FileHandler()
        self.statistics = CompressionStatistics()
        
        # Estado actual
        self.current_file: str = ""
        self.current_text: str = ""
        self.compressed_data: dict = {}
        self.decompressed_text: str = ""
    
    # ============================================
    # 📌 CARGAR ARCHIVOS
    # ============================================
    
    def on_load_text_file(self, file_path: str):
        """
        Carga un archivo de texto.
        
        Args:
            file_path: ruta del archivo
        """
        # Validar ruta
        if not file_path or not file_path.strip():
            self.view.show_message("Error", "Debe seleccionar un archivo", "error")
            return
        
        # Validar que sea archivo .txt
        if not validators.is_valid_text_file(file_path):
            self.view.show_message("Error", "Archivo incompatible. Debe ser .txt", "error")
            return
        
        # Validar que exista y sea legible
        success, error = self.file_handler.validate_file(file_path)
        if not success:
            self.view.show_message("Error", error, "error")
            return
        
        # Leer archivo
        success, content, error = self.file_handler.read_file(file_path)
        if not success:
            self.view.show_message("Error", error, "error")
            return
        
        # Guardar contenido
        self.current_file = file_path
        self.current_text = content
        
        # Actualizar vista
        filename = os.path.basename(file_path)
        self.view.update_file_label(filename)
        self.view.show_message("Éxito", "Archivo cargado correctamente", "success")
    
    def on_load_compressed_file(self, file_path: str):
        """
        Carga un archivo .lz78 comprimido.
        
        Args:
            file_path: ruta del archivo .lz78
        """
        # Validar ruta
        if not file_path or not file_path.strip():
            self.view.show_message("Error", "Debe seleccionar un archivo", "error")
            return
        
        # Validar que sea archivo .lz78
        if not validators.is_valid_lz78_file(file_path):
            self.view.show_message("Error", "Formato incorrecto. Debe ser .lz78", "error")
            return
        
        # Cargar archivo comprimido
        success, codes, dictionary, original_size, error = file_format.load_compressed(file_path)
        if not success:
            self.view.show_message("Error", error, "error")
            return
        
        # Guardar datos
        self.current_file = file_path
        self.compressed_data = {
            'codes': codes,
            'dictionary': dictionary,
            'original_size': original_size
        }
        
        # Actualizar vista
        filename = os.path.basename(file_path)
        self.view.update_file_label(filename)
        self.view.display_dictionary(dictionary, codes)
        self.view.show_message("Éxito", "Archivo .lz78 cargado correctamente", "success")
    
    # ============================================
    # 📌 COMPRESIÓN
    # ============================================
    
    def on_compress(self):
        """
        Comprime el archivo de texto cargado.
        """
        # Validar que haya contenido
        if not self.current_text or not self.current_text.strip():
            self.view.show_message("Error", "Carga un archivo de texto primero", "error")
            return
        
        try:
            # Comprimir
            codes, dictionary, _ = self.compressor.compress(self.current_text)
            
            # Guardar datos
            original_size = len(self.current_text.encode('utf-8'))
            compressed_size = self._calculate_compressed_size(codes, dictionary)
            
            self.compressed_data = {
                'codes': codes,
                'dictionary': dictionary,
                'original_size': original_size
            }
            
            # Mostrar diccionario
            self.view.display_dictionary(dictionary, codes)
            
            # Mostrar estadísticas
            self.view.update_statistics(original_size, compressed_size)
            
            self.view.show_message("Éxito", "Archivo comprimido exitosamente", "success")
        
        except Exception as e:
            self.view.show_message("Error", f"Error al comprimir: {str(e)}", "error")
    
    # ============================================
    # 📌 DESCOMPRESIÓN
    # ============================================
    
    def on_decompress(self):
        """
        Descomprime el archivo .lz78 cargado.
        """
        # Validar que haya datos comprimidos
        if not self.compressed_data or not self.compressed_data.get('codes'):
            self.view.show_message("Error", "Carga un archivo .lz78 primero", "error")
            return
        
        try:
            # Obtener datos
            codes = self.compressed_data['codes']
            dictionary = self.compressed_data['dictionary']
            
            # Descomprimir
            text = self.compressor.decompress(codes, dictionary)
            
            # Guardar texto descomprimido
            self.decompressed_text = text
            
            # Mostrar diccionario
            self.view.display_dictionary(dictionary, codes)
            
            # Mostrar estadísticas
            original_size = self.compressed_data['original_size']
            compressed_size = self._calculate_compressed_size(codes, dictionary)
            self.view.update_statistics(original_size, compressed_size)
            
            self.view.show_message("Éxito", "Archivo descomprimido exitosamente", "success")
        
        except Exception as e:
            self.view.show_message("Error", f"Error al descomprimir: {str(e)}", "error")
    
    # ============================================
    # 📌 GUARDAR ARCHIVOS
    # ============================================
    
    def on_save_compressed(self, file_path: str):
        """
        Guarda el archivo comprimido en formato .lz78.
        
        Args:
            file_path: ruta donde guardar
        """
        # Validar que haya datos comprimidos
        if not self.compressed_data or not self.compressed_data.get('codes'):
            self.view.show_message("Error", "Comprime un archivo primero", "error")
            return
        
        if not file_path or not file_path.strip():
            self.view.show_message("Error", "Debe especificar una ruta", "error")
            return
        
        try:
            # Obtener datos
            codes = self.compressed_data['codes']
            dictionary = self.compressed_data['dictionary']
            original_size = self.compressed_data['original_size']
            
            # Guardar
            success, error = file_format.save_compressed(file_path, codes, dictionary, original_size)
            
            if not success:
                self.view.show_message("Error", error, "error")
                return
            
            filename = os.path.basename(file_path)
            self.view.show_message("Éxito", f"Archivo guardado como {filename}", "success")
        
        except Exception as e:
            self.view.show_message("Error", f"Error al guardar: {str(e)}", "error")
    
    def on_save_decompressed(self, file_path: str):
        """
        Guarda el archivo descomprimido en formato .txt.
        
        Args:
            file_path: ruta donde guardar
        """
        # Validar que haya texto descomprimido
        if not self.decompressed_text or not self.decompressed_text.strip():
            self.view.show_message("Error", "Descomprime un archivo primero", "error")
            return
        
        if not file_path or not file_path.strip():
            self.view.show_message("Error", "Debe especificar una ruta", "error")
            return
        
        try:
            # Guardar archivo
            success, error = self.file_handler.write_file(file_path, self.decompressed_text)
            
            if not success:
                self.view.show_message("Error", error, "error")
                return
            
            filename = os.path.basename(file_path)
            self.view.show_message("Éxito", f"Archivo guardado como {filename}", "success")
        
        except Exception as e:
            self.view.show_message("Error", f"Error al guardar: {str(e)}", "error")
    
    # ============================================
    # 🔧 UTILIDADES
    # ============================================
    
    def _calculate_compressed_size(self, codes: list, dictionary: dict) -> int:
        """
        Calcula el tamaño del archivo comprimido.
        
        Optimización: caracteres ASCII = 1 byte, extendidos = 1 + 1 + bytes
        
        Estructura:
        - Header: 8 bytes
        - Códigos: 4 bytes + (2 + char_encoding) * num_códigos
        """
        size = 8  # Header
        size += 4  # número de códigos
        
        for idx, char in codes:
            size += 2  # idx (2 bytes)
            
            if not char:
                size += 1  # Carácter vacío: 1 byte
            elif len(char) == 1 and ord(char) < 128:
                size += 1  # ASCII: 1 byte
            else:
                char_bytes = char.encode('utf-8')
                size += 1 + 1 + len(char_bytes)  # Marca + len + bytes
        
        return size
