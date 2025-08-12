import os
import subprocess
import platform
from tkinter import filedialog
from typing import Optional
import customtkinter as ctk

def update_log(log_textbox: ctk.CTkTextbox, message: str) -> None:

    log_textbox.insert("0.0", f"● {message}\n\n")


def open_output_folder(folder_path: str, log_textbox: ctk.CTkTextbox) -> None:

    if not folder_path or not os.path.exists(folder_path):
        update_log(log_textbox, "Erro: Pasta de saída inválida ou não selecionada.")
        return
    try:
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", folder_path], check=True)
        else:
            subprocess.run(["xdg-open", folder_path], check=True)
    except Exception as e:
        update_log(log_textbox, f"Não foi possível abrir a pasta: {e}")


def select_image_path() -> Optional[str]:

    return filedialog.askopenfilename(
        title="Selecione um arquivo de imagem",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp")]
    )


def select_output_folder() -> Optional[str]:
    
    return filedialog.askdirectory(title="Selecione a pasta de saída")
