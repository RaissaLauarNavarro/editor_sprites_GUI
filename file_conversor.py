from tkinter import filedialog, messagebox
from PIL import Image
import os


def convert_image_type(image_path: str, output_folder: str, file_type: str, output_name: str) -> str:
    """
    Converte a imagem para o formato escolhido e salva na pasta de saída.
    Retorna o caminho do arquivo convertido ou lança uma exceção.
    """

    try:
        img = Image.open(image_path)
        output_path = os.path.join(output_folder, f"{output_name}.{file_type}")
        img.save(output_path, file_type.upper())
        return output_path
    except Exception as e:
        return ""