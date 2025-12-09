# Vista: Interfaz gráfica principal

# src/view/main_window.py
import tkinter as tk
from tkinter import scrolledtext
from typing import Optional, Dict, List, Tuple
from src.view import dialogs, styles

class MainWindow(tk.Tk):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.current_file: str = ""
        self.compressed_data: Optional[dict] = None
        self.decompressed_text: str = ""

        # widgets
        self.file_label: Optional[tk.Label] = None
        self.dictionary_text: Optional[tk.Text] = None
        self.original_size_label: Optional[tk.Label] = None
        self.compressed_size_label: Optional[tk.Label] = None
        self.compression_ratio_label: Optional[tk.Label] = None
        self.saved_bytes_label: Optional[tk.Label] = None

        self.title("Compresor LZ78")
        self.geometry('900x700')
        bg_color = styles.COLORS.get('bg', '#f0f0f0')
        self.configure(bg=bg_color)

        self.setup_ui()

    def setup_ui(self):
        top_frame = tk.Frame(self, bg=styles.COLORS.get('bg', '#f0f0f0'))
        top_frame.pack(fill='x', padx=styles.PADDING['large'], pady=(20,10))

        self.file_label = tk.Label(top_frame, text="📁 Archivo actual: [Sin archivo]", font=styles.FONTS['label'], bg=styles.COLORS.get('bg','#f0f0f0'))
        self.file_label.pack(side='left')

        btn_frame = tk.Frame(top_frame, bg=styles.COLORS.get('bg','#f0f0f0'))
        btn_frame.pack(side='right')

        btn_load_txt = tk.Button(btn_frame, text="Cargar TXT", command=self.on_load_text_file)
        styles.apply_button_style(btn_load_txt)
        btn_load_txt.pack(side='left', padx=5)

        btn_load_lz = tk.Button(btn_frame, text="Cargar .lz78", command=self.on_load_compressed_file)
        styles.apply_button_style(btn_load_lz)
        btn_load_lz.pack(side='left', padx=5)

        # Dictionary area
        dict_frame = tk.Frame(self, bg=styles.COLORS.get('frame_bg','#ffffff'))
        styles.apply_frame_style(dict_frame)
        dict_frame.pack(fill='both', expand=False, padx=styles.PADDING['large'], pady=10)

        dict_label = tk.Label(dict_frame, text='DICCIONARIO (Índice -> Secuencia)', font=styles.FONTS['title'], bg=styles.COLORS.get('frame_bg','#ffffff'))
        dict_label.pack(anchor='w')

        self.dictionary_text = tk.Text(dict_frame, height=12, font=styles.FONTS['text'])
        self.dictionary_text.pack(fill='both', expand=True)
        self.dictionary_text.config(state='disabled')

        # Actions
        actions_frame = tk.Frame(self, bg=styles.COLORS.get('bg','#f0f0f0'))
        actions_frame.pack(fill='x', padx=styles.PADDING['large'], pady=10)

        btn_compress = tk.Button(actions_frame, text="Comprimir", command=self.on_compress)
        styles.apply_button_style(btn_compress)
        btn_compress.pack(side='left', padx=8)

        btn_decompress = tk.Button(actions_frame, text="Descomprimir", command=self.on_decompress)
        styles.apply_button_style(btn_decompress)
        btn_decompress.pack(side='left', padx=8)

        # Statistics
        stats_frame = tk.Frame(self, bg=styles.COLORS.get('frame_bg','#ffffff'))
        styles.apply_frame_style(stats_frame)
        stats_frame.pack(fill='x', padx=styles.PADDING['large'], pady=10)

        stats_title = tk.Label(stats_frame, text='ESTADÍSTICAS', font=styles.FONTS['title'], bg=styles.COLORS.get('frame_bg','#ffffff'))
        stats_title.grid(row=0, column=0, columnspan=2, sticky='w')

        tk.Label(stats_frame, text='Tamaño Original:', font=styles.FONTS['label'], bg=styles.COLORS.get('frame_bg','#ffffff')).grid(row=1, column=0, sticky='w')
        self.original_size_label = tk.Label(stats_frame, text='0 bytes', font=styles.FONTS['label'], bg=styles.COLORS.get('frame_bg','#ffffff'))
        self.original_size_label.grid(row=1, column=1, sticky='e')

        tk.Label(stats_frame, text='Tamaño Comprimido:', font=styles.FONTS['label'], bg=styles.COLORS.get('frame_bg','#ffffff')).grid(row=2, column=0, sticky='w')
        self.compressed_size_label = tk.Label(stats_frame, text='0 bytes', font=styles.FONTS['label'], bg=styles.COLORS.get('frame_bg','#ffffff'))
        self.compressed_size_label.grid(row=2, column=1, sticky='e')

        tk.Label(stats_frame, text='Ratio de Compresión:', font=styles.FONTS['label'], bg=styles.COLORS.get('frame_bg','#ffffff')).grid(row=3, column=0, sticky='w')
        self.compression_ratio_label = tk.Label(stats_frame, text='0 %', font=styles.FONTS['label'], bg=styles.COLORS.get('frame_bg','#ffffff'))
        self.compression_ratio_label.grid(row=3, column=1, sticky='e')

        tk.Label(stats_frame, text='Bytes Ahorrados:', font=styles.FONTS['label'], bg=styles.COLORS.get('frame_bg','#ffffff')).grid(row=4, column=0, sticky='w')
        self.saved_bytes_label = tk.Label(stats_frame, text='0 bytes', font=styles.FONTS['label'], bg=styles.COLORS.get('frame_bg','#ffffff'))
        self.saved_bytes_label.grid(row=4, column=1, sticky='e')

        # Save buttons
        save_frame = tk.Frame(self, bg=styles.COLORS.get('bg','#f0f0f0'))
        save_frame.pack(fill='x', padx=styles.PADDING['large'], pady=10)

        btn_save_comp = tk.Button(save_frame, text='Guardar Comprimido', command=self.on_save_compressed)
        styles.apply_button_style(btn_save_comp)
        btn_save_comp.pack(side='left', padx=8)

        btn_save_txt = tk.Button(save_frame, text='Guardar TXT', command=self.on_save_decompressed)
        styles.apply_button_style(btn_save_txt)
        btn_save_txt.pack(side='left', padx=8)

    # UI helpers
    def update_file_label(self, file_path: str):
        self.current_file = file_path
        display = file_path if file_path else '[Sin archivo]'
        self.file_label.config(text=f"📁 Archivo actual: {display}")

    def display_dictionary(self, dictionary: Dict[int, str], codes: List[Tuple[int,str]]):
        self.dictionary_text.config(state='normal')
        self.dictionary_text.delete('1.0', tk.END)

        header = "Índice | Secuencia\n"
        header += "------------------------------\n"
        self.dictionary_text.insert(tk.END, header)
        for idx in sorted(dictionary.keys()):
            seq = dictionary[idx]
            line = f"{idx:6} | {repr(seq)}\n"
            self.dictionary_text.insert(tk.END, line)

        self.dictionary_text.insert(tk.END, "\nCÓDIGOS (idx, char):\n")
        for i, code in enumerate(codes, start=1):
            self.dictionary_text.insert(tk.END, f"{i:4}: {code}\n")

        self.dictionary_text.config(state='disabled')

    def update_statistics(self, original_size: int, compressed_size: int):
        try:
            compression_ratio = 0.0
            if original_size > 0:
                compression_ratio = (original_size - compressed_size) / original_size * 100
        except Exception:
            compression_ratio = 0.0

        saved = original_size - compressed_size
        saved_text = f"{saved} bytes" if saved >= 0 else f"Expansión: {-saved} bytes"

        self.original_size_label.config(text=f"{original_size} bytes")
        self.compressed_size_label.config(text=f"{compressed_size} bytes")
        self.compression_ratio_label.config(text=f"{compression_ratio:.2f} %")
        self.saved_bytes_label.config(text=saved_text)

    def show_message(self, title: str, message: str, msg_type: str = 'info'):
        if msg_type == 'error':
            dialogs.show_error(title, message)
        elif msg_type == 'success':
            dialogs.show_success(title, message)
        else:
            dialogs.show_info(title, message)

    # Button handlers (llaman al controlador)
    def on_load_text_file(self):
        path = dialogs.select_text_file()
        if not path:
            return
        if self.controller and hasattr(self.controller, 'on_load_text_file'):
            self.controller.on_load_text_file(path)
        else:
            self.show_message('Info', f'Se seleccionó: {path}', 'info')

    def on_load_compressed_file(self):
        path = dialogs.select_compressed_file()
        if not path:
            return
        if self.controller and hasattr(self.controller, 'on_load_compressed_file'):
            self.controller.on_load_compressed_file(path)
        else:
            self.show_message('Info', f'Se seleccionó comprimido: {path}', 'info')

    def on_compress(self):
        if self.controller and hasattr(self.controller, 'on_compress'):
            self.controller.on_compress()
        else:
            self.show_message('Error', 'No hay controlador conectado para comprimir', 'error')

    def on_decompress(self):
        if self.controller and hasattr(self.controller, 'on_decompress'):
            self.controller.on_decompress()
        else:
            self.show_message('Error', 'No hay controlador conectado para descomprimir', 'error')

    def on_save_compressed(self):
        path = dialogs.save_file_dialog('.lz78')
        if not path:
            return
        if self.controller and hasattr(self.controller, 'on_save_compressed'):
            self.controller.on_save_compressed(path)
        else:
            self.show_message('Info', f'Se guardaría comprimido en: {path}', 'info')

    def on_save_decompressed(self):
        path = dialogs.save_file_dialog('.txt')
        if not path:
            return
        if self.controller and hasattr(self.controller, 'on_save_decompressed'):
            self.controller.on_save_decompressed(path)
        else:
            self.show_message('Info', f'Se guardaría TXT en: {path}', 'info')
