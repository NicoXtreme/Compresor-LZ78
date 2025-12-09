# Modelo: Implementación del algoritmo LZ78 OPTIMIZADO

class LZ78Compressor:
    def __init__(self, max_dict_size=4096):
        """
        Compresor LZ78 (Lempel-Ziv 1978).
        
        Algoritmo:
        - Mantener diccionario de secuencias vistas
        - Para cada posición, encontrar la secuencia más larga que existe
        - Emitir (índice_dict, nuevo_char)
        - Agregar nueva secuencia al diccionario
        """
        self.max_dict_size = max_dict_size
        self.reset()

    def reset(self):
        self.dictionary = {}  # {índice: secuencia}
        self.codes = []  # lista de (índice, carácter)
        self.next_index = 1  # Próximo índice disponible

    # ============================================================
    # 📌 COMPRESIÓN LZ78
    # ============================================================
    def compress(self, text: str):
        """
        Comprime usando LZ78.
        
        Estructura:
        1. Mantener secuencia actual (búsqueda en diccionario)
        2. Extender mientras esté en diccionario
        3. Cuando no está: emitir (índice_actual, nuevo_char)
        4. Agregar nueva secuencia al diccionario
        
        Retorna:
            codes: lista de tuplas (índice, carácter)
            dictionary: diccionario generado
            compressed_string: string serializado
        """
        self.reset()

        if not text:
            raise ValueError("El texto está vacío")

        pos = 0

        while pos < len(text):
            current_idx = 0  # Índice actual en diccionario (0 = inicio)
            start_pos = pos

            # Extender mientras la secuencia esté en el diccionario
            while pos < len(text):
                char = text[pos]
                # Buscar si (current_idx, char) forma una secuencia en dict
                next_idx = self._find_sequence(current_idx, char)

                if next_idx > 0:
                    # Secuencia encontrada, seguir extendiendo
                    current_idx = next_idx
                    pos += 1
                else:
                    # Secuencia no existe, emitir código
                    break

            # Emitir código: (índice_encontrado, nuevo_carácter)
            if pos < len(text):
                new_char = text[pos]
                self.codes.append((current_idx, new_char))

                # Agregar nueva secuencia al diccionario
                if self.next_index <= self.max_dict_size:
                    prev_seq = self.dictionary.get(current_idx, "")
                    new_seq = prev_seq + new_char
                    self.dictionary[self.next_index] = new_seq
                    self.next_index += 1

                pos += 1
            else:
                # Fin del texto: si queda algo, emitir
                if current_idx > 0:
                    self.codes.append((current_idx, ""))

        return self.codes, self.dictionary, self._codes_to_string()

    # ============================================================
    # 📌 DESCOMPRESIÓN LZ78
    # ============================================================
    def decompress(self, codes: list, dictionary: dict) -> str:
        """
        Descomprime códigos LZ78.
        
        Para cada código (índice, carácter):
        - Si índice = 0: carácter literal
        - Si índice > 0: tomar diccionario[índice] + carácter
        """
        result = ""

        for index, char in codes:
            if index == 0:
                # Carácter literal
                result += char
            else:
                # Prefijo del diccionario + nuevo carácter
                prefix = dictionary.get(index, "")
                result += prefix + char

        return result

    # ============================================================
    # ⚙️ UTILIDADES
    # ============================================================
    def _find_sequence(self, prefix_idx: int, char: str) -> int:
        """
        Busca en el diccionario si existe la secuencia
        diccionario[prefix_idx] + char
        
        Retorna el índice si existe, 0 si no.
        """
        prefix = self.dictionary.get(prefix_idx, "")
        target_seq = prefix + char

        for idx, seq in self.dictionary.items():
            if seq == target_seq:
                return idx

        return 0

    def _codes_to_string(self) -> str:
        """Serializa códigos a string."""
        parts = []
        for idx, char in self.codes:
            # Escapar caracteres especiales
            safe_char = char.replace("|", "\\|").replace(";", "\\;")
            parts.append(f"{idx}|{safe_char}")
        return ";".join(parts)

    def get_dictionary_info(self):
        """Info del diccionario."""
        entries = len(self.dictionary)
        size_bytes = sum(len(seq) for seq in self.dictionary.values())

        if entries == 0:
            compression_rate = 0.0
        else:
            compression_rate = (entries / size_bytes) * 100 if size_bytes > 0 else 0.0

        return {
            "size": size_bytes,
            "entries": entries,
            "compression_rate": round(compression_rate, 2)
        }

