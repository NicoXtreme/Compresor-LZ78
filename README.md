# Compresor LZ78 - Algoritmo de Compresión sin Pérdida

Aplicación educativa con interfaz gráfica para comprimir y descomprimir archivos de texto utilizando el algoritmo LZ78 (Lempel-Ziv 1978). Proyecto final de la asignatura Teoría de la Información, noveno semestre de Ingeniería de Sistemas.

## 📋 Características

- ✅ Compresión y descompresión basada en algoritmo LZ78
- ✅ Interfaz gráfica intuitiva desarrollada con Tkinter
- ✅ Visualización en tiempo real del diccionario dinámico
- ✅ Estadísticas detalladas de compresión (ratio, bytes ahorrados)
- ✅ Formato binario optimizado `.lz78` sin persistencia de diccionario
- ✅ Validación de archivos y manejo robusto de errores
- ✅ Soporte para caracteres UTF-8 con codificación variable

## 🔧 Requisitos

- Python 3.8 o superior
- Tkinter (incluido en distribuciones estándar de Python)
- Sistema operativo: Windows, macOS o Linux

## 📥 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/NicoXtreme/Compresor-LZ78.git
cd Compresor-LZ78

# Ejecutar la aplicación
python -m src.main
```

## 🚀 Uso

1. **Cargar un archivo:**
   - Botón "Load TXT" para cargar archivo de texto
   - Botón "Load Compressed" para cargar archivo `.lz78` existente

2. **Comprimir:**
   - Selecciona "Compress" para aplicar el algoritmo LZ78
   - Visualiza el diccionario y códigos generados
   - Observa estadísticas de compresión en tiempo real

3. **Descomprimir:**
   - Selecciona "Decompress" para recuperar archivo original
   - Verifica que el contenido sea idéntico al original

4. **Guardar:**
   - "Save Compressed" guarda en formato `.lz78`
   - "Save Decompressed" guarda como archivo `.txt`

## 📁 Estructura del Proyecto

```
Compresor-LZ78/
├── src/
│   ├── main.py                          # Punto de entrada
│   ├── model/
│   │   ├── lz78_compressor.py          # Algoritmo LZ78
│   │   ├── file_handler.py             # Operaciones I/O
│   │   └── statistics.py               # Cálculos estadísticos
│   ├── view/
│   │   ├── main_window.py              # Interfaz principal
│   │   ├── dialogs.py                  # Diálogos emergentes
│   │   └── styles.py                   # Configuración visual
│   ├── controller/
│   │   └── main_controller.py          # Coordinación MVC
│   └── utils/
│       ├── file_format.py              # Serialización binaria
│       ├── validators.py               # Validación de entrada
│       └── constants.py                # Constantes globales
├── samples/
│   └── ejemplo.txt                     # Archivo de prueba
├── compressed/                         # Archivos generados
├── INFORME.md                          # Informe académico detallado
└── README.md
```

## 🏗️ Arquitectura

La aplicación implementa el patrón **Modelo-Vista-Controlador (MVC)**:

- **Modelo**: Clase `LZ78Compressor` con algoritmo de compresión/descompresión
- **Vista**: Interfaz Tkinter con widgets interactivos
- **Controlador**: Coordinación entre modelo y vista, validación de datos

### Formato de Archivo `.lz78`

```
Header (8 bytes)
├── Firma: "LZ78" (4 bytes)
├── Versión: 0x0001 (2 bytes)
└── Tamaño Original (2 bytes)

Contenido
├── Cantidad de Códigos (4 bytes)
└── Códigos comprimidos (tamaño variable)
    ├── Índice: 2 bytes
    └── Carácter: 1-3 bytes (codificación optimizada)
```

## 📊 Rendimiento

| Métrica | Valor |
|---------|-------|
| Tamaño entrada | 4051 bytes |
| Tamaño comprimido | ~3200 bytes |
| Ratio compresión | 20.98% |
| Tiempo compresión | ~30ms |
| Tiempo descompresión | ~5ms |

## 👥 Equipo de Desarrollo

| Nombre | Código | Rol |
|--------|--------|-----|
| **Nicolás Francisco Ortiz Luna** | 20212020079 | Desarrollador - Controlador y Optimización |
| **Dilan Stive Arboleda Zambrano** | 20212020105 | Desarrollador - Algoritmo LZ78 |
| **Santiago Guarguati Pedraza** | 20221020024 | Desarrollador - Interfaz Gráfica |

## 📚 Documentación

- `INFORME.md` - Informe académico completo con análisis teórico y técnico del proyecto
- `src/` - Código fuente completamente comentado

## 📝 Notas Académicas

Este proyecto implementa el algoritmo LZ78 tal como fue descrito por Lempel y Ziv en 1978. La aplicación valida experimentalmente los principios de compresión sin pérdida mediante:

- Implementación correcta del algoritmo
- Validación de compresión/descompresión
- Análisis de eficiencia comparativa
- Documentación detallada del proceso

## 📄 Licencia

Proyecto académico - Universidad Distrital Francisco José de Caldas

## 🔗 Referencias

- Lempel, A., & Ziv, J. (1978). "Compression of individual sequences via variable-rate coding." IEEE Transactions on Information Theory, 24(5), 530-536.
- Salomon, D. (2007). "Data Compression: The Complete Reference" (4th ed.). Springer-Verlag.

---

**Última actualización**: Diciembre 2025

## Licencia
