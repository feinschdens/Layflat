# Datei: generate_image_pdf.py

from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from PIL import Image
import glob
import os

# Konstanten definieren
PAGE_WIDTH = 300 * mm  # Breite der PDF-Seite in Millimetern
PAGE_HEIGHT = 300 * mm  # Höhe der PDF-Seite in Millimetern
MARGIN = 20 * mm  # Abstand vom Rand der Seite in Millimetern
PADDING = 5 * mm  # Abstand zwischen den Bildern in Millimetern
IMAGE_SIZE = 50 * mm  # Kurze Seite des Bildes in Millimetern

# Verfügbare Fläche für Bilder berechnen
usable_width = PAGE_WIDTH - 2 * MARGIN  # Verfügbare Breite unter Berücksichtigung der Ränder
usable_height = PAGE_HEIGHT - 2 * MARGIN  # Verfügbare Höhe unter Berücksichtigung der Ränder

def get_scaled_dimensions(image):
    """Berechnet die neuen Abmessungen eines Bildes,
    sodass die kurze Seite 50 mm beträgt und das Seitenverhältnis beibehalten wird."""
    width, height = image.size  # Originalabmessungen des Bildes
    if width < height:
        new_width = IMAGE_SIZE
        new_height = IMAGE_SIZE * height / width
    else:
        new_height = IMAGE_SIZE
        new_width = IMAGE_SIZE * width / height
    return new_width, new_height

def create_pdf(image_paths, output_path):
    """Erstellt eine PDF-Datei aus einer Liste von Bildpfaden."""
    # Neues PDF-Dokument mit der angegebenen Seitengröße erstellen
    c = canvas.Canvas(output_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Anfangsposition für die Bilder setzen
    x = MARGIN
    y = PAGE_HEIGHT - MARGIN

    # Durch alle Bildpfade iterieren
    for idx, img_path in enumerate(image_paths):
        print(f"Verarbeite Bild {idx + 1} von {len(image_paths)}: {img_path}")
        try:
            img = Image.open(img_path)  # Bild öffnen
        except Exception as e:
            print(f"Fehler beim Öffnen des Bildes {img_path}: {e}")
            continue

        img_width, img_height = get_scaled_dimensions(img)  # Bildabmessungen skalieren
        print(f"Bildgröße nach Skalierung: {img_width} x {img_height}")

        # Überprüfen, ob das Bild auf die aktuelle Zeile passt, ansonsten Zeile wechseln
        if x + img_width > PAGE_WIDTH - MARGIN:
            x = MARGIN
            y -= (img_height + PADDING)
            print(f"Zeile gewechselt: x={x}, y={y}")

        # Überprüfen, ob das Bild auf die aktuelle Seite passt, ansonsten neue Seite erstellen
        if y - img_height < MARGIN:
            c.showPage()  # Neue Seite einfügen
            x = MARGIN
            y = PAGE_HEIGHT - MARGIN
            print("Neue Seite erstellt")

        # Bild auf der PDF-Seite platzieren
        try:
            c.drawImage(img_path, x, y - img_height, width=img_width, height=img_height)
            print(f"Bild platziert: x={x}, y={y}")
        except Exception as e:
            print(f"Fehler beim Einfügen des Bildes {img_path} in das PDF: {e}")
            continue

        x += img_width + PADDING  # x-Position für das nächste Bild aktualisieren

    c.save()  # PDF speichern
    print(f"PDF erfolgreich erstellt: {output_path}")

# Liste der Bildpfade erhalten (Pfad anpassen)
image_paths = glob.glob('C:\\Users\\peter\\Pictures\\Familie\\Familie\\**\\*.jpg', recursive=True) + \
              glob.glob('C:\\Users\\peter\\Pictures\\Familie\\Familie\\**\\*.jpeg', recursive=True) + \
              glob.glob('C:\\Users\\peter\\Pictures\\Familie\\Familie\\**\\*.png', recursive=True) + \
              glob.glob('C:\\Users\\peter\\Pictures\\Familie\\Familie\\**\\*.dng', recursive=True)  # Pfad für Windows

# Überprüfen, ob Bilder gefunden wurden
if not image_paths:
    print("Keine Bilder gefunden. Überprüfe den Pfad.")
else:
    # PDF erstellen
    create_pdf(image_paths, 'output.pdf')  # Ausgabe-PDF-Datei erstellen
