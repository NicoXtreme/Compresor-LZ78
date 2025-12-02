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

#### 1. **`src/model/lz78_compressor.py`** (Algoritmo Principal)

**Clase: `LZ78Compressor`**

**Atributos:**
```python
- dictionary: dict  # {índice: (índice_anterior, carácter)}
- codes: list       # [(índice_anterior, nuevo_carácter), ...]
- next_code: int    # Siguiente código a asignar (comienza en 1)
- max_dict_size: int  # Límite del diccionario
```

**Métodos:**

1. `__init__(max_dict_size=4096)`
   - Inicializa diccionario vacío
   - Inicializa lista de códigos vacía
   - next_code = 1
   - Diccionario base: caracteres ASCII (0-255)

2. `compress(text: str) -> tuple`
   - Entrada: texto a comprimir
   - Salida: `(codes: list, dictionary: dict, compressed_text: str)`
   - **Funcionamiento:**
     - Iterar caracteres
     - Buscar secuencia más larga en diccionario
     - Cuando no encuentra, guardar código y añadir nueva secuencia
     - Retornar códigos y diccionario generado

3. `decompress(codes: list, dictionary: dict) -> str`
   - Entrada: códigos y diccionario
   - Salida: texto original
   - Reconstruir usando diccionario inverso

4. `get_dictionary_info() -> dict`
   - Retorna: `{size: int, entries: int, compression_rate: float}`
   - Size: tamaño en bytes del diccionario
   - Entries: número de entradas
   - Compression_rate: porcentaje de compresión

---

#### 2. **`src/model/file_handler.py`** (Manejo de Archivos)

**Clase: `FileHandler`**

**Atributos:**
```python
- current_file: str      # Ruta del archivo actual
- content: str           # Contenido cargado
- file_encoding: str     # Encoding usado (utf-8)
```

**Métodos:**

1. `__init__()`
   - Inicializar atributos en None/""/utf-8

2. `read_file(path: str) -> tuple`
   - Entrada: ruta del archivo
   - Salida: `(success: bool, content: str, error_msg: str)`
   - **Validaciones:**
     - Archivo existe
     - Archivo es legible (try/except)
     - Archivo no está vacío
   - **Errores posibles:**
     - "Archivo no encontrado"
     - "Archivo vacío"
     - "Error al leer el archivo"

3. `write_file(path: str, content: str) -> tuple`
   - Entrada: ruta y contenido
   - Salida: `(success: bool, error_msg: str)`
   - Escribir archivo con encoding utf-8
   - **Errores posibles:**
     - "Error al escribir el archivo"
     - "Ruta inválida"

4. `validate_file(path: str) -> tuple`
   - Entrada: ruta del archivo
   - Salida: `(is_valid: bool, error_msg: str)`
   - Verificar: existe, es legible, no vacío
   - Retornar (True, "") si es válido

---

#### 3. **`src/utils/file_format.py`** (Formato .lz78 Personalizado)

**Estructura del archivo .lz78:**
```
[HEADER: 8 bytes]
├─ Firma: "LZ78" (4 bytes)
├─ Versión: 1 (2 bytes)
└─ Tamaño original: int (2 bytes)

[DICTIONARY: Variable]
├─ Número de entradas: int (4 bytes)
└─ Para cada entrada:
    ├─ Índice: int (2 bytes)
    └─ Tupla (idx_anterior, carácter): string

[CODES: Variable]
├─ Número de códigos: int (4 bytes)
└─ Códigos comprimidos: lista serializada
```

**Funciones:**

1. `save_compressed(file_path: str, codes: list, dictionary: dict, original_size: int) -> tuple`
   - Entrada: ruta, códigos, diccionario, tamaño original
   - Salida: `(success: bool, error_msg: str)`
   - Serializar estructura completa
   - Escribir en formato binario o JSON

2. `load_compressed(file_path: str) -> tuple`
   - Entrada: ruta del archivo .lz78
   - Salida: `(success: bool, codes: list, dictionary: dict, original_size: int, error_msg: str)`
   - Leer y deserializar archivo
   - Validar header
   - **Errores posibles:**
     - "Formato incorrecto"
     - "Archivo corrupto"
     - "Versión no soportada"

3. `is_valid_lz78_file(file_path: str) -> bool`
   - Verificar que archivo tiene header correcto

---

#### 4. **`src/utils/constants.py`** (Constantes)

```python
# Extensiones válidas
VALID_TEXT_EXTENSIONS = ['.txt']
VALID_COMPRESSED_EXTENSIONS = ['.lz78']

# Límites
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_DICTIONARY_SIZE = 4096
MIN_FILE_SIZE = 1  # 1 byte

# Formato
LZ78_FORMAT_VERSION = 1
LZ78_HEADER_SIZE = 8
LZ78_SIGNATURE = b'LZ78'

# Encoding
DEFAULT_ENCODING = 'utf-8'
```

---

## 🎨 SANTIAGO: Interfaz Gráfica

### Archivos a Modificar

#### 1. **`src/view/main_window.py`** (Ventana Principal)

**Clase: `MainWindow`** (hereda de `tk.Tk`)

**Atributos:**
```python
- controller: MainController  # Referencia al controlador
- current_file: str          # Archivo actual cargado
- compressed_data: dict      # {codes, dictionary, original_size}
- decompressed_text: str     # Texto descomprimido

# Widgets principales
- file_label: tk.Label       # Muestra archivo actual
- dictionary_text: tk.Text   # Muestra diccionario
- stats_frame: tk.Frame      # Marco con estadísticas
- original_size_label: tk.Label
- compressed_size_label: tk.Label
- compression_ratio_label: tk.Label
- saved_bytes_label: tk.Label
```

**Estructura del Layout:**

```
┌─────────────────────────────────────────────────┐
│  Compresor LZ78                      [X]        │
├─────────────────────────────────────────────────┤
│                                                  │
│  📁 Archivo actual: [Sin archivo]               │
│                                                  │
│  ┌─ CARGA DE ARCHIVOS ──────────────────────┐  │
│  │ [Cargar TXT]  [Cargar .lz78 comprimido]  │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ┌─ DICCIONARIO ────────────────────────────┐  │
│  │ Índice│Anterior│Carácter│Código         │  │
│  │ 0     │  -     │  A     │  0            │  │
│  │ 1     │  0     │  B     │  1            │  │
│  │ ...                                     │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ┌─ ACCIONES ────────────────────────────────┐ │
│  │ [Comprimir]  [Descomprimir]              │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ ESTADÍSTICAS ────────────────────────────┐ │
│  │ Tamaño Original:    1000 bytes           │ │
│  │ Tamaño Comprimido:   350 bytes           │ │
│  │ Ratio de Compresión: 65%                 │ │
│  │ Bytes Ahorrados:     650 bytes           │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ GUARDAR RESULTADOS ──────────────────────┐ │
│  │ [Guardar Comprimido]  [Guardar TXT]      │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Métodos:**

1. `__init__(controller: MainController)`
   - Crear ventana Tkinter
   - Crear todos los widgets
   - Conectar botones a controlador
   - Título: "Compresor LZ78"
   - Tamaño: 800x700 píxeles

2. `setup_ui()`
   - Crear marco principal
   - Crear secciones (carga, diccionario, acciones, estadísticas, guardado)
   - Aplicar estilos

3. `update_file_label(file_path: str)`
   - Actualizar etiqueta con nombre del archivo

4. `display_dictionary(dictionary: dict, codes: list)`
   - Limpiar `dictionary_text`
   - Mostrar tabla/lista del diccionario
   - Formato: "Índice | Anterior | Carácter | Código"

5. `update_statistics(original_size: int, compressed_size: int)`
   - Calcular ratio y bytes ahorrados
   - Actualizar las 4 etiquetas de estadísticas

6. `show_message(title: str, message: str, msg_type: str)`
   - msg_type: 'error', 'info', 'success'
   - Llamar a funciones de dialogs.py

7. Métodos de botones (llaman al controlador):
   - `on_load_text_file()` → llama `controller.on_load_text_file()`
   - `on_load_compressed_file()` → llama `controller.on_load_compressed_file()`
   - `on_compress()` → llama `controller.on_compress()`
   - `on_decompress()` → llama `controller.on_decompress()`
   - `on_save_compressed()` → llama `controller.on_save_compressed()`
   - `on_save_decompressed()` → llama `controller.on_save_decompressed()`

---

#### 2. **`src/view/dialogs.py`** (Diálogos)

**Funciones Principales:**

1. `show_error(title: str, message: str)`
   - Usar `messagebox.showerror()`
   - Muestra mensaje de error en diálogo emergente
   - Ejemplos:
     - "Archivo vacío"
     - "Formato incorrecto"
     - "Archivo incompatible"
     - "Error en lectura/escritura"

2. `show_info(title: str, message: str)`
   - Usar `messagebox.showinfo()`
   - Muestra información general

3. `show_success(title: str, message: str)`
   - Usar `messagebox.showinfo()` con icono de éxito
   - Confirma operación completada

4. `select_text_file() -> str`
   - Usar `filedialog.askopenfilename()`
   - Filtro: "Archivos de texto (*.txt)"
   - Retorna: ruta del archivo o string vacío si cancela

5. `select_compressed_file() -> str`
   - Usar `filedialog.askopenfilename()`
   - Filtro: "Archivos LZ78 (*.lz78)"
   - Retorna: ruta del archivo o string vacío

6. `save_file_dialog(extension: str) -> str`
   - Entrada: extensión (.txt o .lz78)
   - Usar `filedialog.asksaveasfilename()`
   - Retorna: ruta para guardar o string vacío

---

#### 3. **`src/view/styles.py`** (Estilos)

**Definir esquema de colores:**

```python
COLORS = {
    'bg': '#f0f0f0',           # Fondo gris claro
    'fg': '#333333',           # Texto oscuro
    'button_bg': '#4CAF50',    # Botones verdes
    'button_fg': '#ffffff',    # Texto botones blanco
    'error': '#f44336',        # Rojo para errores
    'success': '#4CAF50',      # Verde para éxito
    'info': '#2196F3',         # Azul para info
    'frame_bg': '#ffffff',     # Marco blanco
    'label_bg': '#e0e0e0',     # Etiquetas gris
}

FONTS = {
    'title': ('Arial', 16, 'bold'),
    'label': ('Arial', 11),
    'button': ('Arial', 10, 'bold'),
    'text': ('Courier New', 10),
}

PADDING = {
    'standard': 10,
    'large': 20,
}
```

**Función:**

- `apply_button_style(button: tk.Button)`
  - Aplicar colores y fuentes a botones
  - Padding: 10px
  - Ancho: 20 caracteres

- `apply_frame_style(frame: tk.Frame)`
  - Aplicar color de fondo
  - Padding interno

---

#### 4. **`src/main.py`** (Punto de Entrada)

**Estructura:**

```python
from src.view.main_window import MainWindow
from src.controller.main_controller import MainController

def main():
    """Inicia la aplicación"""
    root = MainWindow()
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Responsabilidades:**
- Crear instancia de MainWindow
- Iniciar loop de Tkinter
- Punto de entrada de la aplicación

---

## 📊 NICOLAS: Controlador y Lógica

### Archivos a Modificar

#### 1. **`src/controller/main_controller.py`** (Controlador Principal - MVC)

**Clase: `MainController`**

**Atributos:**
```python
- view: MainWindow              # Referencia a la vista
- compressor: LZ78Compressor    # Instancia del compresor
- file_handler: FileHandler     # Manejador de archivos
- statistics: CompressionStatistics  # Calculador de estadísticas
- validators: module            # Módulo de validadores

# Estado actual
- current_file: str             # Ruta del archivo actual
- current_text: str             # Contenido cargado
- compressed_data: dict         # {codes, dictionary, original_size}
- decompressed_text: str        # Texto descomprimido
```

**Métodos:**

1. `__init__(view: MainWindow)`
   - Inicializar todas las instancias
   - Guardar referencia a la vista
   - Conectar eventos de vista a métodos del controlador

2. `on_load_text_file(file_path: str)`
   - **Flujo:**
     1. Validar ruta (no vacía)
     2. Usar `file_handler.validate_file(file_path)` - verificar que existe, no vacío, legible
     3. Si error → mostrar error en vista con `view.show_message()`
     4. Si OK → leer archivo con `file_handler.read_file(file_path)`
     5. Guardar contenido en `self.current_text`
     6. Actualizar label en vista: `view.update_file_label(file_path)`
     7. Mostrar success: "Archivo cargado correctamente"

3. `on_load_compressed_file(file_path: str)`
   - **Flujo:**
     1. Validar ruta
     2. Usar `validators.is_valid_lz78_file(file_path)`
     3. Si error → mostrar error
     4. Si OK → usar `file_format.load_compressed(file_path)`
     5. Guardar en `self.compressed_data` = {codes, dictionary, original_size}
     6. Actualizar label: `view.update_file_label(file_path)`
     7. Mostrar diccionario: `view.display_dictionary(dictionary, codes)`
     8. Mostrar success: "Archivo .lz78 cargado"

4. `on_compress()`
   - **Flujo:**
     1. Validar que `self.current_text` no esté vacío
     2. Si vacío → mostrar error: "Carga un archivo primero"
     3. Comprimir: `codes, dictionary = self.compressor.compress(self.current_text)`
     4. Guardar en `self.compressed_data`
     5. Calcular tamaño comprimido (serializar)
     6. Mostrar diccionario: `view.display_dictionary(dictionary, codes)`
     7. Mostrar estadísticas:
        - `original_size = len(self.current_text.encode('utf-8'))`
        - `compressed_size = calcular_tamaño_serializado(codes, dictionary)`
        - `view.update_statistics(original_size, compressed_size)`
     8. Mostrar success: "Archivo comprimido exitosamente"

5. `on_decompress()`
   - **Flujo:**
     1. Validar que `self.compressed_data` no esté vacío
     2. Si vacío → mostrar error: "Carga un archivo .lz78 primero"
     3. Obtener: `codes = self.compressed_data['codes']`, `dictionary = self.compressed_data['dictionary']`
     4. Descomprimir: `text = self.compressor.decompress(codes, dictionary)`
     5. Guardar en `self.decompressed_text = text`
     6. Mostrar diccionario descomprimido
     7. Mostrar estadísticas de descompresión
     8. Mostrar success: "Archivo descomprimido"

6. `on_save_compressed(file_path: str)`
   - **Flujo:**
     1. Validar que `self.compressed_data` no esté vacío
     2. Si vacío → mostrar error: "Comprime un archivo primero"
     3. Obtener datos: `codes, dictionary, original_size = self.compressed_data`
     4. Guardar: `file_format.save_compressed(file_path, codes, dictionary, original_size)`
     5. Si error → mostrar error
     6. Si OK → mostrar success: "Archivo guardado como [nombre].lz78"

7. `on_save_decompressed(file_path: str)`
   - **Flujo:**
     1. Validar que `self.decompressed_text` no esté vacío
     2. Si vacío → mostrar error: "Descomprime un archivo primero"
     3. Escribir: `file_handler.write_file(file_path, self.decompressed_text)`
     4. Si error → mostrar error
     5. Si OK → mostrar success: "Archivo guardado como [nombre].txt"

---

#### 2. **`src/model/statistics.py`** (Estadísticas de Compresión)

**Clase: `CompressionStatistics`**

**Métodos:**

1. `__init__()`
   - Sin atributos especiales

2. `calculate(original_size: int, compressed_size: int) -> dict`
   - **Entrada:** 
     - original_size: bytes
     - compressed_size: bytes
   - **Salida:** diccionario con:
     ```python
     {
         'original_size': int,        # bytes
         'compressed_size': int,      # bytes
         'compression_ratio': float,  # porcentaje 0-100
         'saved_bytes': int,          # original - compressed
         'expansion_ratio': float,    # si es negativo (archivo creció)
     }
     ```
   - **Cálculos:**
     - `compression_ratio = (original_size - compressed_size) / original_size * 100`
     - `saved_bytes = original_size - compressed_size`

3. `format_statistics(stats: dict) -> str`
   - Entrada: diccionario de estadísticas
   - Retorna: string formateado para mostrar
   - Ejemplo: "Tamaño original: 1000 bytes\nTamaño comprimido: 350 bytes\n..."

---

#### 3. **`src/utils/validators.py`** (Validadores)

**Funciones:**

1. `is_valid_text_file(path: str) -> bool`
   - Verificar que:
     - Archivo existe: `os.path.exists(path)`
     - Tiene extensión .txt: `path.endswith('.txt')`
   - Retorna: True/False

2. `is_valid_lz78_file(path: str) -> bool`
   - Verificar que:
     - Archivo existe
     - Tiene extensión .lz78
     - Header es correcto (primeros 4 bytes = "LZ78")
   - Retorna: True/False

3. `is_empty_file(path: str) -> bool`
   - Verificar tamaño del archivo: `os.path.getsize(path) == 0`
   - Retorna: True si está vacío, False si tiene contenido

4. `is_readable_file(path: str) -> bool`
   - Intentar abrir archivo en modo lectura
   - Si funciona: retorna True
   - Si error: retorna False

5. `validate_file_content(content: str, max_size: int = 10485760) -> tuple`
   - Entrada: contenido y tamaño máximo (10 MB por defecto)
   - Salida: `(is_valid: bool, error_msg: str)`
   - Validar:
     - No vacío
     - Tamaño menor a máximo
     - Encoding UTF-8 válido
   - Retorna: (True, "") si OK, (False, "mensaje") si error

---

#### 4. **Flujo de Integración Esperado**

```
Usuario carga archivo TXT
        ↓
on_load_text_file(path)
├─ file_handler.validate_file(path)
├─ file_handler.read_file(path)
├─ view.update_file_label(path)
└─ view.show_message("success", "Cargado")

Usuario presiona "Comprimir"
        ↓
on_compress()
├─ compressor.compress(text)
├─ estadísticas = statistics.calculate(...)
├─ view.display_dictionary(dictionary, codes)
├─ view.update_statistics(...)
└─ view.show_message("success", "Comprimido")

Usuario presiona "Guardar Comprimido"
        ↓
on_save_compressed(path)
├─ file_format.save_compressed(...)
├─ file_handler.write_file(...)
└─ view.show_message("success", "Guardado")
```

---

## 🔗 Conexión entre Desarrolladores

- **Dilan** proporciona: LZ78Compressor, FileHandler, formato .lz78
- **Santiago** proporciona: ventana principal, diálogos, estilos
- **Nicolas** usa: lo de Dev 1 y Dev 2 para conectarlos en el controlador

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

1. **Dilan** implementa algoritmo y manejo de archivos
2. **Santiago** crea la interfaz gráfica
3. **Nicolas** implementa controlador que une todo
4. **Todos** prueban y corrigen errores
