from PIL import Image
from typing import Tuple

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Converte uma cor hexadecimal em uma tupla RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def replace_color(image: Image.Image, old_color_rgb: Tuple[int, int, int], new_color_rgb: Tuple[int, int, int], tolerance: int = 30) -> Image.Image:
    """
    Substitui todas as ocorrências de uma cor por outra em uma imagem, com tolerância.
    """
    img_copy = image.copy().convert("RGBA")
    data = img_copy.load()
    width, height = img_copy.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = data[x, y]
            # Distância de cor (L2 simples)
            if ((r - old_color_rgb[0])**2 + (g - old_color_rgb[1])**2 + (b - old_color_rgb[2])**2) ** 0.8 <= tolerance:
                data[x, y] = new_color_rgb + (a,)

    return img_copy
