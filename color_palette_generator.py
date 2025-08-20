from PIL import Image
from colorthief import ColorThief
from typing import List, Tuple
import math

def get_color_palette(image_path: str, num_colors: int = 16, min_distance: int = 50) -> List[str]:
    """
    Gera uma paleta de cores a partir de uma imagem, removendo cores muito parecidas.

    Args:
        image_path: Caminho para a imagem.
        num_colors: Número máximo de cores na paleta.
        min_distance: Distância mínima entre cores no espaço RGB (0-441 aprox).

    Returns:
        Lista de cores hexadecimais.
    """
    try:
        color_thief = ColorThief(image_path)
        raw_palette = color_thief.get_palette(color_count=num_colors*2)  
        filtered_palette = []
        for color in raw_palette:
            if all(color_distance(color, c) >= min_distance for c in filtered_palette):
                filtered_palette.append(color)
            if len(filtered_palette) >= num_colors:
                break

        return [rgb_to_hex(color) for color in filtered_palette]
    except Exception as e:
        raise Exception(f"Erro ao gerar a paleta de cores: {e}")

def color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Calcula a distância Euclidiana entre duas cores RGB."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Converte RGB em hexadecimal."""
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
