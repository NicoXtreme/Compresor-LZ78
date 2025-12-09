# Modelo: Cálculo de estadísticas de compresión


class CompressionStatistics:
    """
    Calcula y maneja las estadísticas de compresión.
    """
    
    def __init__(self):
        """Inicializa la clase de estadísticas."""
        pass
    
    def calculate(self, original_size: int, compressed_size: int) -> dict:
        """
        Calcula estadísticas de compresión.
        
        Args:
            original_size: tamaño original en bytes
            compressed_size: tamaño comprimido en bytes
        
        Returns:
            dict con:
                - original_size: int
                - compressed_size: int
                - compression_ratio: float (porcentaje 0-100)
                - saved_bytes: int
                - expansion_ratio: float (negativo si creció)
        """
        if original_size == 0:
            return {
                'original_size': 0,
                'compressed_size': compressed_size,
                'compression_ratio': 0.0,
                'saved_bytes': -compressed_size,
                'expansion_ratio': float('inf') if compressed_size > 0 else 0.0
            }
        
        saved_bytes = original_size - compressed_size
        compression_ratio = (saved_bytes / original_size) * 100
        expansion_ratio = ((compressed_size - original_size) / original_size) * 100
        
        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': round(compression_ratio, 2),
            'saved_bytes': saved_bytes,
            'expansion_ratio': round(expansion_ratio, 2)
        }
    
    def format_statistics(self, stats: dict) -> str:
        """
        Formatea las estadísticas para mostrar en la interfaz.
        
        Args:
            stats: diccionario de estadísticas
        
        Returns:
            string formateado
        """
        original = stats['original_size']
        compressed = stats['compressed_size']
        ratio = stats['compression_ratio']
        saved = stats['saved_bytes']
        
        result = f"Tamaño original:    {original} bytes\n"
        result += f"Tamaño comprimido:  {compressed} bytes\n"
        result += f"Ratio de compresión: {ratio}%\n"
        result += f"Bytes ahorrados:    {saved} bytes"
        
        return result
