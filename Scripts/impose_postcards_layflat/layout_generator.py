# layout_generator.py

"""
layout_generator.py

Modul zur Generierung von Layouts für die Druckbögen.
Funktionen:
- generate_layouts(images, backprint): Generiert die Layouts für die Druckbögen.
"""

from PIL import Image

def generate_layouts(images, backprint):
    """
    Generiert die Layouts für die Druckbögen.
    Args:
        images (list): Liste der Bilder.
        backprint (Image): Rückseitendatei.
    Returns:
        list: Liste der generierten Layouts.
    """
    layouts = []
    # Beispiel für die Layout-Generierung, genaue Logik muss hier implementiert werden
    for i in range(0, len(images), 6):  # Raster 2x3
        layout = Image.new("RGB", (640, 305))
        for j in range(6):
            if i + j < len(images):
                img = images[i + j]
                # Platzierung und Rotation der Bilder
                layout.paste(img, (j % 3 * 155, j // 3 * 105))
        layouts.append(layout)
    return layouts
