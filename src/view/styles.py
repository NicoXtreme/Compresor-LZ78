# Vista: Estilos y temas para la interfaz

# Esquema de estilos para la UI

COLORS = {
    'bg': '#f0f0f0',
    'fg': '#333333',
    'button_bg': '#4CAF50',
    'button_fg': '#ffffff',
    'error': '#f44336',
    'success': '#4CAF50',
    'info': '#2196F3',
    'frame_bg': '#ffffff',
    'label_bg': '#e0e0e0',
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

import tkinter as tk

def apply_button_style(button: tk.Button):
    button.config(
        bg=COLORS['button_bg'],
        fg=COLORS['button_fg'],
        font=FONTS['button'],
        padx=10,
        pady=6,
        width=18,
        relief='raised',
        bd=2,
    )

def apply_frame_style(frame: tk.Frame):
    frame.config(
        bg=COLORS['frame_bg'],
        padx=PADDING['standard'],
        pady=PADDING['standard'],
        bd=1,
        relief='flat',
    )
