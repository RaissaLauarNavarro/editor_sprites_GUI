import customtkinter as ctk
from main_controller import MainController
from gui_builder import GUIBuilder

class App(ctk.CTk):
    """
    Aplicativo principal "Editor de Sprites".
    Gerencia a janela e coordena a interação entre a GUI e o controlador.
    """
    def __init__(self) -> None:
        super().__init__()

        # Inicializa o controlador antes de construir a UI
        self.controller = MainController(self)

        self.title("Editor de Sprites")
        self.geometry("1100x650")
        self.minsize(800, 600)
        self._set_appearance_mode("dark")
        self.configure(fg_color=self.controller.COLOR_BACKGROUND)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        GUIBuilder.build(self, self.controller)
        self.controller._initialize()

if __name__ == "__main__":
    app = App()
    app.mainloop()