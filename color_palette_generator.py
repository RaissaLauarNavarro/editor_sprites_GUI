from PIL import Image
from colorthief import ColorThief
from typing import List, Tuple
import math
import io

def color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Calcula a distância Euclidiana entre duas cores RGB."""
    # (r1-r2)^2 + (g1-g2)^2 + (b1-b2)^2
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Converte RGB em hexadecimal."""
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


def get_color_palette(image: Image.Image, num_colors: int = 24, min_distance: int = 20) -> List[str]:
    """
    Gera uma paleta de cores a partir de uma imagem, removendo cores muito parecidas.
    """
    try:
        with io.BytesIO() as stream:
            image_rgb = image.copy().convert("RGB")
            image_rgb.save(stream, format='PNG')
            stream.seek(0)

            color_thief = ColorThief(stream)
            raw_palette = color_thief.get_palette(color_count=num_colors * 3, quality=9)

        if not raw_palette:
            return []

        filtered_palette = []
        # verifica se a cor está suficientemente distante das já selecionadas
        for color in raw_palette:
            if all(color_distance(color, existing_color) >= min_distance for existing_color in filtered_palette):
                filtered_palette.append(color)
            
            if len(filtered_palette) >= num_colors:
                break

        return [rgb_to_hex(color) for color in filtered_palette]
    except Exception as e:
        raise Exception(f"Erro ao gerar a paleta de cores: {e}")