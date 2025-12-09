# Modelo: Implementación del algoritmo LZ78

class LZ78Compressor:
    def __init__(self, max_dict_size=4096):
        """
        Inicializa el compresor LZ78.

        Diccionario base:
            índice → cadena
        Ejemplo inicial:
            {1: 'A', 2: 'B', ... 256: <caracter ASCII>}
        """
        self.max_dict_size = max_dict_size
        self.reset()

    # -------------------------------
    # 🔄 Reiniciar estructuras internas
    # -------------------------------
    def reset(self):
        self.dictionary = {}     # {index: string}
        self.codes = []          # [(index_prev, new_char)]
        self.next_code = 1       # índice del diccionario

    # -------------------------------
    # 📌 COMPRESIÓN LZ78
    # -------------------------------
    def compress(self, text: str):
        """
        Comprime un texto usando LZ78.

        Retorna:
            codes: lista de tuplas (índice, carácter)
            dictionary: diccionario final generado
            compressed_string: representación serializada
        """
        self.reset()

        if not text:
            raise ValueError("El texto está vacío")

        current = ""

        for char in text:
            if current + char in self.dictionary.values():
                current += char
            else:
                # Encontrar índice del prefijo actual
                index = self._find_index(current)

                # Guardar código
                self.codes.append((index, char))

                # Agregar nueva secuencia al diccionario
                if self.next_code <= self.max_dict_size:
                    self.dictionary[self.next_code] = current + char
                    self.next_code += 1

                current = ""

        # Si queda algo pendiente
        if current:
            index = self._find_index(current)
            self.codes.append((index, ""))

        # Convertir a formato texto para guardar
        compressed_str = self._codes_to_string()

        return self.codes, self.dictionary, compressed_str

    # -------------------------------
    # 📌 DESCOMPRESIÓN LZ78
    # -------------------------------
    def decompress(self, codes: list, dictionary: dict) -> str:
        """
        Descomprime una lista de códigos usando el diccionario generado.
        """
        result = ""

        for index, char in codes:
            if index == 0:
                entry = char
            else:
                entry = dictionary[index]
                if char:
                    entry = entry + char
            result += entry

        return result

    # -------------------------------
    # ⚙️ Utilidades internas
    # -------------------------------
    def _find_index(self, sequence: str) -> int:
        """ Devuelve el índice del diccionario para una secuencia. """
        for idx, seq in self.dictionary.items():
            if seq == sequence:
                return idx
        return 0

    def _codes_to_string(self) -> str:
        """
        Serializa los códigos a un string para guardarlo en .lz78
        Formato:
            index|char;index|char;...
        """
        out = []
        for idx, ch in self.codes:
            ch = ch.replace("|", "\\|")  # Escape por seguridad
            out.append(f"{idx}|{ch}")
        return ";".join(out)

    # -------------------------------
    # 📊 Información del diccionario
    # -------------------------------
    def get_dictionary_info(self):
        size_bytes = sum(len(v) for v in self.dictionary.values())
        entries = len(self.dictionary)

        if size_bytes == 0:
            compression_rate = 0.0
        else:
            # Cálculo básico: tamaño comprimido vs tamaño diccionario
            compression_rate = (entries / size_bytes) * 100

        return {
            "size": size_bytes,
            "entries": entries,
            "compression_rate": round(compression_rate, 2)
        }

