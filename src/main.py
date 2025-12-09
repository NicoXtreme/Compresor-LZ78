# Punto de entrada principal de la aplicación

from src.view.main_window import MainWindow
from src.controller.main_controller import MainController


def main():
    """
    Inicia la aplicación.
    """
    # Crear ventana principal
    root = MainWindow()
    
    # Crear controlador
    controller = MainController(root)
    
    # Asignar controlador a la vista
    root.controller = controller
    
    # Iniciar loop principal
    root.mainloop()


if __name__ == "__main__":
    main()
