import os
from PIL import Image, ImageOps
from typing import Callable

def process_and_save_blocks(
    image_path: str,
    output_folder: str,
    bloco_px: int,
    escala: int,
    progress_callback: Callable[[float], None]
) -> None:
    """
    Processa uma imagem, dividindo-a em blocos e salvando-os.

    Args:
        image_path: Caminho para a imagem de entrada.
        output_folder: Caminho da pasta onde os blocos serão salvos.
        bloco_px: O tamanho de cada bloco em pixels.
        escala: O fator de escala para redimensionar os blocos.
        progress_callback: Uma função para notificar o progresso (de 0 a 1).
    """
    # Lógica de processamento e salvamento
    imagem = Image.open(image_path).convert("RGBA")
    largura, altura = imagem.size
    
    if largura % bloco_px != 0 or altura % bloco_px != 0:
        raise ValueError(f"Dimensões ({largura}x{altura}) não são múltiplas de {bloco_px}px.")

    contador = 0
    total_rows = altura // bloco_px
    nome_base = os.path.splitext(os.path.basename(image_path))[0]
    
    for i, y in enumerate(range(0, altura, bloco_px)):
        for x in range(0, largura, bloco_px):
            bloco = imagem.crop((x, y, x + bloco_px, y + bloco_px))
            if bloco.getbbox():  # Salva apenas blocos com pixels não transparentes
                if escala > 1:
                    bloco = bloco.resize((bloco_px * escala, bloco_px * escala), Image.Resampling.NEAREST)
                nome_arquivo = f"{nome_base}_{contador:04}.png"
                bloco.save(os.path.join(output_folder, nome_arquivo))
                contador += 1
        
        progress = (i + 1) / total_rows
        progress_callback(progress)

