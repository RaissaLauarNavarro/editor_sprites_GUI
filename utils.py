import os
import subprocess
import platform
from tkinter import filedialog
from typing import Optional
import customtkinter as ctk

def update_log(log_textbox: ctk.CTkTextbox, message: str, status_label: Optional[ctk.CTkLabel] = None) -> None:
    """
    Adiciona uma nova mensagem ao log e, opcionalmente, atualiza um rótulo de status.
    """
    log_textbox.insert("0.0", f"● {message}\n\n")
    if status_label:
        status_label.configure(text=message, text_color="white")


def open_output_folder(folder_path: str, log_textbox: ctk.CTkTextbox, status_label: Optional[ctk.CTkLabel] = None) -> None:
    """
    Tenta abrir a pasta de saída no explorador de arquivos do sistema.
    """
    if not folder_path or not os.path.exists(folder_path):
        update_log(log_textbox, "Erro: Pasta de saída inválida ou não selecionada.", status_label)
        return
    try:
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", folder_path], check=True)
        else:
            subprocess.run(["xdg-open", folder_path], check=True)
    except Exception as e:
        update_log(log_textbox, f"Não foi possível abrir a pasta: {e}", status_label)


def select_image_path() -> Optional[str]:
    """
    Abre a caixa de diálogo para selecionar um arquivo de imagem.
    Retorna o caminho do arquivo ou None se a seleção for cancelada.
    """
    return filedialog.askopenfilename(
        title="Selecione um arquivo de imagem",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif *.webp"), ("Todos os arquivos", "*.*")]
    )


def select_output_folder() -> Optional[str]:
    """
    Abre a caixa de diálogo para selecionar a pasta de saída.
    Retorna o caminho da pasta ou None se a seleção for cancelada.
    """
    return filedialog.askdirectory(title="Selecione a pasta de saída")