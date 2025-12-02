# Tareas para cada uno - Compresor LZ78

## 🔧 Instrucciones de Trabajo en Git

### Configuración Inicial (Todos)

```bash
# Clonar repositorio
git clone https://github.com/NicoXtreme/Compresor-LZ78.git
cd Compresor-LZ78

# Crear tu rama personal
# Ejemplo
git checkout -b feat/dilan-lz78-algorithm
# O para Santiago: git checkout -b feat/santiago-gui
# O para Nicolas: git checkout -b feat/nicolas-controller
```

### Flujo de Trabajo

1. **Trabajar en tu rama:**
   ```bash
   git pull origin master  # Traer cambios antes de empezar
   # ... hacer cambios ...
   ```

2. **Hacer commit frecuentemente:**
   ```bash
   git add .
   git commit -m "FEAT: descripción de lo que hiciste"
   ```

3. **Publicar tu rama:**
   ```bash
   git push origin feat/[tu-rama]
   ```

4. **Crear Pull Request en GitHub:**
   - Ir a https://github.com/NicoXtreme/Compresor-LZ78
   - Click en "Pull requests" → "New pull request"
   - Seleccionar tu rama (feat/dilan-lz78-algorithm) como origen
   - Seleccionar "master" como destino
   - Agregar descripción de cambios
   - Click en "Create Pull Request"

5. **NICOLAS revisa y hace merge:**
   - NICOLAS es el revisor y responsable del merge final a master
   - Verifica que el código sea correcto
   - Aprueba y hace merge
   - Elimina la rama después del merge

---

## 👨‍💻 DILAN: Algoritmo LZ78

### Archivos a Modificar

1. **`src/model/lz78_compressor.py`**
   - Crear clase `LZ78Compressor`
   - Método `compress(text: str)` → retorna (códigos, diccionario)
   - Método `decompress(codes, dictionary)` → retorna texto original
   - Método `get_dictionary_info()` → información del diccionario

2. **`src/model/file_handler.py`**
   - Crear clase `FileHandler`
   - Método `read_file(path)` → retorna contenido del archivo
   - Método `write_file(path, content)` → guarda contenido
   - Método `validate_file(path)` → retorna (es_válido, mensaje_error)
   - Validar que archivo no esté vacío
   - Validar que archivo sea legible

3. **`src/utils/file_format.py`**
   - Función `save_compressed(file_path, codes, dictionary, original_size)` → guarda en formato .lz78
   - Función `load_compressed(file_path)` → retorna (codes, dictionary, original_size)
   - Estructura: HEADER + DICTIONARY + CODES

4. **`src/utils/constants.py`**
   - Constantes de extensiones válidas (.txt)
   - Constante de límites de tamaño
   - Constante de versión del formato .lz78

---

## 🎨 SANTIAGO: Interfaz Gráfica

### Archivos a Modificar

1. **`src/view/main_window.py`**
   - Crear clase `MainWindow` con Tkinter
   - **Sección Carga:**
     - Botón "Cargar Archivo de Texto"
     - Botón "Cargar Archivo Comprimido (.lz78)"
     - Label mostrando archivo actual
   - **Sección Compresión:**
     - Botón "Comprimir"
     - Área para mostrar diccionario (tabla o texto)
   - **Sección Descompresión:**
     - Botón "Descomprimir"
     - Área para mostrar diccionario descomprimido
   - **Sección Estadísticas:**
     - Tamaño original (bytes)
     - Tamaño comprimido (bytes)
     - Porcentaje de compresión (%)
     - Bytes ahorrados
   - **Sección Guardado:**
     - Botón "Guardar Archivo Comprimido"
     - Botón "Guardar Archivo Descomprimido"

2. **`src/view/dialogs.py`**
   - `show_error(title, message)` → muestra errores
   - `show_info(title, message)` → muestra información
   - `show_success(title, message)` → muestra éxito
   - `select_file()` → abre diálogo para seleccionar archivo .txt
   - `select_compressed_file()` → abre diálogo para seleccionar archivo .lz78
   - `save_file_dialog(title, extension)` → abre diálogo para guardar archivo
   - Mensajes de error específicos:
     - "Archivo vacío"
     - "Formato incorrecto"
     - "Archivo incompatible"
     - "Error en lectura/escritura"

3. **`src/view/styles.py`**
   - Colores, fuentes, tamaños
   - Tema consistente

4. **`src/main.py`**
   - Función `main()` que inicia la aplicación Tkinter
   - Punto de entrada: `if __name__ == "__main__": main()`

---

## 📊 NICOLAS: Controlador y Lógica

### Archivos a Modificar

1. **`src/controller/main_controller.py`**
   - Crear clase `MainController`
   - Método `on_load_text_file(file_path)` → valida y carga archivo .txt
   - Método `on_load_compressed_file(file_path)` → carga archivo .lz78
   - Método `on_compress()` → comprime el archivo cargado
   - Método `on_decompress()` → descomprime archivo .lz78 cargado
   - Método `on_save_compressed(file_path)` → guarda archivo comprimido
   - Método `on_save_decompressed(file_path)` → guarda archivo descomprimido
   - Manejo de errores para todos los métodos

2. **`src/model/statistics.py`**
   - Crear clase `CompressionStatistics`
   - Método `calculate(original_size, compressed_size)` → retorna dict con:
     - `original_size`: bytes
     - `compressed_size`: bytes
     - `compression_ratio`: porcentaje (0-100)
     - `saved_bytes`: bytes ahorrados

3. **`src/utils/validators.py`**
   - `is_valid_text_file(path)` → valida extensión .txt
   - `is_valid_lz78_file(path)` → valida formato .lz78
   - `is_empty_file(path)` → verifica si archivo está vacío
   - `is_readable_file(path)` → verifica si es legible

---

## 🔗 Conexión entre Desarrolladores

- **Dev 1** proporciona: LZ78Compressor, FileHandler, formato .lz78
- **Dev 2** proporciona: ventana principal, diálogos, estilos
- **Dev 3** usa: lo de Dev 1 y Dev 2 para conectarlos en el controlador

El controlador (Dev 3) es el intermediario que conecta la interfaz (Dev 2) con el algoritmo (Dev 1).

---

## Requisitos Funcionales Cubiertos

✅ **a)** Capturar un archivo de texto  
✅ **b)** Comprimir con LZ78 y mostrar diccionario  
✅ **c)** Guardar archivo comprimido en formato .lz78  
✅ **d)** Validar que archivo no esté vacío y sea legible  
✅ **e)** Cargar archivos previamente comprimidos con LZ78  
✅ **f)** Descomprimir y mostrar diccionario  
✅ **g)** Generar archivo con diccionario y mensaje codificado  
✅ **h)** Guardar archivo descomprimido  
✅ **i)** Mostrar estadísticas: tamaño original, comprimido, porcentaje, bytes ahorrados  
✅ **j)** Mostrar mensajes de error específicos

---

## Orden de Trabajo Recomendado

1. **Dev 1** implementa algoritmo y manejo de archivos
2. **Dev 2** crea la interfaz gráfica
3. **Dev 3** implementa controlador que une todo
4. **Todos** prueban y corrigen errores
