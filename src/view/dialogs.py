# Vista: Diálogos emergentes (errores, información, etc)

import tkinter as tk
from tkinter import messagebox, filedialog

def show_error(title: str, message: str):
    try:
        messagebox.showerror(title, message)
    except Exception:
        print(f"[ERROR] {title}: {message}")

def show_info(title: str, message: str):
    try:
        messagebox.showinfo(title, message)
    except Exception:
        print(f"[INFO] {title}: {message}")

def show_success(title: str, message: str):
    try:
        messagebox.showinfo(title, message)
    except Exception:
        print(f"[SUCCESS] {title}: {message}")

def select_text_file() -> str:
    path = filedialog.askopenfilename(title="Seleccionar archivo de texto", filetypes=[("Archivos de texto","*.txt")])
    return path or ""

def select_compressed_file() -> str:
    path = filedialog.askopenfilename(title="Seleccionar archivo comprimido LZ78", filetypes=[("Archivos LZ78","*.lz78")])
    return path or ""

def save_file_dialog(extension: str) -> str:
    if not extension.startswith('.'):
        extension = '.' + extension
    return filedialog.asksaveasfilename(defaultextension=extension, filetypes=[(f"Archivo {extension}", f"*{extension}")]) or ""
