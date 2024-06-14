from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from PIL import Image, ExifTags
import glob
import os
from datetime import datetime
from tkinter import Tk, filedialog

# GUI initialisieren
root = Tk()
root.withdraw()  # Hauptfenster ausblenden

# Verzeichnisse auswählen
image_dir = filedialog.askdirectory(title="Wählen Sie das Verzeichnis mit den Bildern")
output_dir = filedialog.askdirectory(title="Wählen Sie das Verzeichnis für die Ausgabepdfs")

# Pfade prüfen
if not image_dir or not output_dir:
    print("Verzeichnisse wurden nicht korrekt ausgewählt.")
    exit(1)

# Konstanten definieren
ORIGINAL_PAGE_WIDTH = 300 * mm  # Originalbreite der PDF-Seite in Millimetern (30 cm)
ORIGINAL_PAGE_HEIGHT = 300 * mm  # Originalhöhe der PDF-Seite in Millimetern (30 cm)
PAGE_WIDTH = 2 * ORIGINAL_PAGE_WIDTH  # Breite der neuen kombinierten PDF-Seite in Millimetern (60 cm)
PAGE_HEIGHT = ORIGINAL_PAGE_HEIGHT  # Höhe der neuen kombinierten PDF-Seite in Millimetern (30 cm)
MARGIN = 20 * mm  # Abstand vom Rand der Seite in Millimetern (2 cm)
PADDING = 5 * mm  # Abstand zwischen den Bildern in Millimetern (0,5 cm)
FRAME_WIDTH = 0.3 * mm  # Breite des Rahmens in Millimetern (0,3 mm)

# Verfügbare Fläche für Bilder berechnen
usable_width = ORIGINAL_PAGE_WIDTH - 2 * MARGIN  # Verfügbare Breite für eine Originalseite unter Berücksichtigung der Ränder
usable_height = ORIGINAL_PAGE_HEIGHT - 2 * MARGIN  # Verfügbare Höhe für eine Originalseite unter Berücksichtigung der Ränder

# Größe der Kachel (inkl. Bild und Abstand)
cell_width = (usable_width - 2 * PADDING) / 3  # Breite einer Kachel im Raster
cell_height = (usable_height - 2 * PADDING) / 3  # Höhe einer Kachel im Raster

# Größe der Bilder innerhalb der Kacheln (Abstand zwischen den Bildern berücksichtigen)
IMAGE_WIDTH = cell_width  # Breite des Bildes
IMAGE_HEIGHT = cell_height  # Höhe des Bildes

# Bildpfade definieren
IMAGE_PATHS_PATTERN = os.path.join(image_dir, '**', '*.{ext}')

def get_scaled_dimensions(image):
    """Berechnet die neuen Abmessungen eines Bildes,
    sodass es in die Rasterzelle passt und das Seitenverhältnis beibehalten wird."""
    width, height = image.size  # Originalabmessungen des Bildes
    ratio = min(IMAGE_WIDTH / width, IMAGE_HEIGHT / height)
    new_width = width * ratio
    new_height = height * ratio
    return new_width, new_height

def correct_orientation(image):
    """Korrigiert die Orientierung des Bildes basierend auf EXIF-Daten."""
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            exif = dict(exif.items())
            orientation = exif.get(orientation, None)
            print(f"EXIF Orientierung: {orientation}")

            if orientation == 3:
                image = image.rotate(180, expand=True)
                print("Bild um 180 Grad gedreht")
            elif orientation == 6:
                image = image.rotate(270, expand=True)
                print("Bild um 270 Grad gedreht")
            elif orientation == 8:
                image = image.rotate(90, expand=True)
                print("Bild um 90 Grad gedreht")
        else:
            print("Keine EXIF-Daten gefunden")
    except (AttributeError, KeyError, IndexError) as e:
        print(f"Fehler bei der Verarbeitung der EXIF-Daten: {e}")
        # Kein EXIF-Tag oder keine Orientierung gefunden
        pass
    return image

def get_image_date(image_path):
    """Liest das Aufnahmedatum aus den EXIF-Daten des Bildes."""
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if exif is not None:
            exif = dict(exif.items())
            for tag, value in exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                if decoded == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        return None
    except Exception as e:
        print(f"Fehler beim Lesen des Aufnahmedatums für {image_path}: {e}")
        return None

def create_pdf(image_paths, output_path_template):
    """Erstellt eine PDF-Datei aus einer Liste von Bildpfaden."""
    # Bilder nach Aufnahmedatum sortieren
    images_with_dates = []
    images_without_dates = []

    for img_path in image_paths:
        date = get_image_date(img_path)
        if date:
            images_with_dates.append((img_path, date))
        else:
            images_without_dates.append(img_path)

    images_with_dates.sort(key=lambda x: x[1])
    sorted_image_paths = [img[0] for img in images_with_dates] + images_without_dates

    part_number = 1
    page_count = 0

    # Neues PDF-Dokument mit der angegebenen Seitengröße erstellen
    c = canvas.Canvas(output_path_template.format(part_number), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    print(f"PDF-Dokument {part_number} erstellt.")

    # Initiale Position für das erste Bild setzen
    x_start = MARGIN
    y_start = PAGE_HEIGHT - MARGIN
    x = x_start
    y = y_start

    # Bildindex für Debug-Zwecke
    img_index = 1

    # Durch alle Bildpfade iterieren
    for idx, img_path in enumerate(sorted_image_paths):
        print(f"Verarbeite Bild {idx + 1} von {len(sorted_image_paths)}: {img_path}")
        try:
            img = Image.open(img_path)  # Bild öffnen
            img = correct_orientation(img)  # Orientierung korrigieren
            img_width, img_height = get_scaled_dimensions(img)  # Bildabmessungen skalieren
            img = img.resize((int(img_width), int(img_height)), Image.LANCZOS)  # Bild skalieren
        except Exception as e:
            print(f"Fehler beim Öffnen des Bildes {img_path}: {e}")
            continue

        print(f"Bildgröße nach Skalierung: {img_width} x {img_height}")

        # Berechnung der freien Räume für Zentrierung
        free_space_x = (cell_width - img_width) / 2
        free_space_y = (cell_height - img_height) / 2

        # Überprüfen, ob das Bild auf die aktuelle Zeile passt, ansonsten Zeile wechseln
        if x + cell_width > PAGE_WIDTH - MARGIN:
            x = x_start
            y -= (cell_height + PADDING)
            print(f"Zeile gewechselt: x={x}, y={y}")

        # Überprüfen, ob das Bild auf die aktuelle Seite passt, ansonsten neue Seite erstellen
        if y - cell_height < MARGIN:
            c.showPage()  # Neue Seite einfügen
            x = x_start
            y = y_start
            page_count += 1
            print("Neue Seite erstellt")

            # Überprüfen, ob die maximale Seitenanzahl erreicht wurde
            if page_count >= 48:  # Maximale Seitenzahl halbiert
                c.save()  # Aktuelles PDF speichern
                part_number += 1
                page_count = 0
                c = canvas.Canvas(output_path_template.format(part_number), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
                print(f"PDF-Dokument {part_number} erstellt.")

        # Bild auf der PDF-Seite platzieren
        try:
            img_path_corrected = f"{img_path}_corrected.jpg"
            img.save(img_path_corrected)
            c.drawImage(img_path_corrected, x + free_space_x, y - img_height - free_space_y, width=img_width, height=img_height)
            print(f"Bild platziert: x={x + free_space_x}, y={y - img_height - free_space_y}")

            # Rahmen um das Bild zeichnen
            c.setStrokeColorRGB(0, 0, 0)  # Schwarz
            c.setLineWidth(FRAME_WIDTH)
            c.rect(x + free_space_x, y - img_height - free_space_y, img_width, img_height)
            print(f"Rahmen gezeichnet: x={x + free_space_x}, y={y - img_height - free_space_y}, width={img_width}, height={img_height}")

            # Entferne das temporäre, korrigierte Bild
            os.remove(img_path_corrected)
        except Exception as e:
            print(f"Fehler beim Einfügen des Bildes {img_path} in das PDF: {e}")
            continue

        x += (cell_width + PADDING)  # x-Position für das nächste Bild aktualisieren
        img_index += 1

    c.save()  # Letztes PDF speichern
    print(f"PDF erfolgreich erstellt: {output_path_template.format(part_number)}")

# Liste der Bildpfade erhalten (Pfad anpassen)
image_extensions = ['jpg', 'jpeg', 'png', 'dng']
image_paths = [glob.glob(IMAGE_PATHS_PATTERN.format(ext=ext), recursive=True) for ext in image_extensions]
image_paths = [item for sublist in image_paths for item in sublist]  # Flache Liste erstellen

# Überprüfen, ob Bilder gefunden wurden
if not image_paths:
    print("Keine Bilder gefunden. Überprüfe den Pfad.")
else:
    print(f"{len(image_paths)} Bilder gefunden.")
    # PDF erstellen
    output_path_template = os.path.join(output_dir, 'output_part{}.pdf')
    create_pdf(image_paths, output_path_template)  # Ausgabe-PDF-Dateien erstellen
