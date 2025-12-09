#!/usr/bin/env python3
"""Script de prueba para verificar compresión/descompresión"""

import json
import sys
sys.path.insert(0, r'c:\Users\nicox\OneDrive\Escritorio\Ing. Sistemas\Noveno Semestre\Teoria de la Informacion\Proyecto Final')

from src.model.lz78_compressor import LZ78Compressor

# Leer archivo original
with open(r'c:\Users\nicox\OneDrive\Escritorio\Ing. Sistemas\Noveno Semestre\Teoria de la Informacion\Proyecto Final\samples\ejemplo.txt', 'r', encoding='utf-8') as f:
    original_text = f.read()

print('=== ARCHIVO ORIGINAL ===')
print(f'Contenido:\n{repr(original_text)}\n')
print(f'Tamaño: {len(original_text)} caracteres')
print(f'Tamaño en bytes: {len(original_text.encode("utf-8"))} bytes\n')

# Cargar archivo .lz78 comprimido
with open(r'c:\Users\nicox\OneDrive\Escritorio\Ing. Sistemas\Noveno Semestre\Teoria de la Informacion\Proyecto Final\samples\ejemplo.lz78', 'r', encoding='utf-8') as f:
    compressed_data = json.load(f)

print('=== ARCHIVO COMPRIMIDO ===')
print(f'Header: {compressed_data["header"]}')
print(f'Número de entradas en diccionario: {len(compressed_data["dictionary"])}')
print(f'Número de códigos: {len(compressed_data["codes"])}\n')

# Reconstruir diccionario en formato correcto
dictionary = {}
for entry in compressed_data['dictionary']:
    dictionary[entry['index']] = entry['sequence']

# Obtener códigos
codes = [(code['idx'], code['char']) for code in compressed_data['codes']]

# Descomprimir
compressor = LZ78Compressor()
decompressed = compressor.decompress(codes, dictionary)

print('=== VERIFICACIÓN ===')
print(f'Texto original: {repr(original_text)}')
print(f'Texto descomprimido: {repr(decompressed)}')
print(f'¿Son iguales? {original_text == decompressed}')

if original_text == decompressed:
    print('\n✅ COMPRESIÓN CORRECTA - El archivo fue comprimido y descomprimido exitosamente')
else:
    print('\n❌ ERROR EN COMPRESIÓN - Los textos no coinciden')
    print(f'Diferencia: original tiene {len(original_text)} chars, descomprimido tiene {len(decompressed)} chars')
