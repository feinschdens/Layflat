import os
import glob
import io
from datetime import datetime
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image, ExifTags
from PyPDF2 import PdfReader, PdfWriter
import fitz  # PyMuPDF
from tkinter import simpledialog, Tk, filedialog

# Registriere die TrueType-Schriftart Arial
arial_path = 'C:/Windows/Fonts/arial.ttf'
pdfmetrics.registerFont(TTFont('Arial', arial_path))

# Neue Funktion zur Einstellung der Standardschriftart
def set_standard_font(c):
    c.setFont('Arial', 12)

# GUI initialisieren
root = Tk()
root.withdraw()  # Hauptfenster ausblenden

# Verzeichnisse auswählen
image_dir = filedialog.askdirectory(title="Wählen Sie das Verzeichnis mit den Bildern")
output_dir = filedialog.askdirectory(title="Wählen Sie das Verzeichnis für die zusammengeführten PDFs")

# Pfade prüfen
if not image_dir or not output_dir:
    print("Verzeichnisse wurden nicht korrekt ausgewählt.")
    exit(1)

# Benutzer nach dem Basisnamen für die gespeicherte Datei fragen
base_filename = simpledialog.askstring("Dateiname", "Wie soll die gespeicherte Datei lauten?")
if not base_filename:
    print("Kein Dateiname angegeben.")
    exit(1)

# Konstanten definieren
PAGE_WIDTH = 300 * mm  # Breite der PDF-Seite in Millimetern (30 cm)
PAGE_HEIGHT = 300 * mm  # Höhe der PDF-Seite in Millimetern (30 cm)
MARGIN = 20 * mm  # Abstand vom Rand der Seite in Millimetern (2 cm)
PADDING = 5 * mm  # Abstand zwischen den Bildern in Millimetern (0,5 cm)
FRAME_WIDTH = 0.3 * mm  # Breite des Rahmens in Millimetern (0,3 mm)

# Verfügbare Fläche für Bilder berechnen
usable_width = PAGE_WIDTH - 2 * MARGIN  # Verfügbare Breite unter Berücksichtigung der Ränder
usable_height = PAGE_HEIGHT - 2 * MARGIN  # Verfügbare Höhe unter Berücksichtigung der Ränder

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
    new_width = int(width * ratio)
    new_height = int(height * ratio)
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

            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return image

def convert_to_rgb(image):
    """Konvertiert das Bild in den RGB-Modus, falls es im RGBA-Modus vorliegt."""
    if image.mode == 'RGBA':
        return image.convert('RGB')
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

def create_pdf(image_paths):
    """Erstellt PDF-Dateien im Speicher aus einer Liste von Bildpfaden."""
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

    pdfs = []
    part_number = 1
    page_count = 0

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # Setze die Schriftart auf die eingebettete Schriftart Arial
    set_standard_font(c)  # Neue Funktion aufrufen

    x_start = MARGIN
    y_start = PAGE_HEIGHT - MARGIN
    x = x_start
    y = y_start

    img_index = 1

    for idx, img_path in enumerate(sorted_image_paths):
        try:
            img = Image.open(img_path)
            img = correct_orientation(img)
            img = convert_to_rgb(img)
            img_width, img_height = get_scaled_dimensions(img)
            img = img.resize((img_width, img_height), Image.LANCZOS)
        except Exception as e:
            print(f"Fehler beim Öffnen des Bildes {img_path}: {e}")
            continue

        free_space_x = (cell_width - img_width) / 2
        free_space_y = (cell_height - img_height) / 2

        if x + cell_width > PAGE_WIDTH - MARGIN:
            x = x_start
            y -= (cell_height + PADDING)

        if y - cell_height < MARGIN:
            c.showPage()
            set_standard_font(c)  # Setze die Schriftart auf jeder neuen Seite
            x = x_start
            y = y_start
            page_count += 1

            if page_count >= 96:
                c.save()
                packet.seek(0)
                pdfs.append(packet)
                packet = io.BytesIO()
                c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
                set_standard_font(c)  # Neue Funktion aufrufen
                part_number += 1
                page_count = 0

        try:
            img_path_corrected = f"{img_path}_corrected.jpg"
            img.save(img_path_corrected, quality=95)
            c.drawImage(img_path_corrected, x + free_space_x, y - img_height - free_space_y, width=img_width, height=img_height)
            
            # Rahmen um das Bild zeichnen
            c.setStrokeColorRGB(0, 0, 0)  # Schwarz
            c.setLineWidth(FRAME_WIDTH)
            c.rect(x + free_space_x, y - img_height - free_space_y, img_width, img_height)

            os.remove(img_path_corrected)
        except Exception as e:
            print(f"Fehler beim Einfügen des Bildes {img_path} in das PDF: {e}")
            continue

        x += (cell_width + PADDING)
        img_index += 1

    c.save()
    packet.seek(0)
    pdfs.append(packet)

    return pdfs

def merge_pages_in_pdf_memory(pdfs, output_folder, base_filename):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    part_number = 1
    for packet in pdfs:
        reader = PdfReader(packet)
        writer = PdfWriter()
        output_filename = f"{base_filename}_{part_number}.pdf"
        output_path = os.path.join(output_folder, output_filename)

        page0 = reader.pages[0]
        original_width = float(page0.mediabox.width)
        original_height = float(page0.mediabox.height)
        merged_width = 2 * original_width

        merged_packet = io.BytesIO()
        can = canvas.Canvas(merged_packet, pagesize=(merged_width, original_height))
        set_standard_font(can)  # Neue Funktion aufrufen
        
        for i in range(0, len(reader.pages), 2):
            img1_path = img2_path = None
            try:
                doc = fitz.open(stream=packet.getvalue(), filetype="pdf")
                page1 = doc.load_page(i)
                pix1 = page1.get_pixmap()
                img1_path = f"page1_{i}.png"
                pix1.save(img1_path)
                
                if i + 1 < len(reader.pages):
                    page2 = doc.load_page(i + 1)
                    pix2 = page2.get_pixmap()
                    img2_path = f"page2_{i + 1}.png"
                    pix2.save(img2_path)
                
                if img1_path:
                    can.drawImage(img1_path, 0, 0, width=original_width, height=original_height)
                if img2_path:
                    can.drawImage(img2_path, original_width, 0, width=original_width, height=original_height)
                
                can.showPage()
                set_standard_font(can)  # Neue Funktion aufrufen

            except Exception as e:
                print(f"Fehler beim Verarbeiten der Seiten {i} und {i + 1}: {e}")
            finally:
                if img1_path and os.path.exists(img1_path):
                    os.remove(img1_path)
                if img2_path and os.path.exists(img2_path):
                    os.remove(img2_path)

        can.save()
        merged_packet.seek(0)

        new_pdf = PdfReader(merged_packet)
        for page in new_pdf.pages:
            writer.add_page(page)

        with open(output_path, 'wb') as output_pdf:
            writer.write(output_pdf)

        part_number += 1

    # Diagnose der generierten PDFs
    for pdf_file in glob.glob(os.path.join(output_folder, "*.pdf")):
        diagnose_pdf(pdf_file)

def diagnose_pdf(pdf_path):
    print(f"Diagnose für Datei: {pdf_path}")
    doc = fitz.open(pdf_path)
    fonts = doc.get_page_fonts(0)
    if not fonts:
        print("Keine Schriftarten gefunden.")
    else:
        for font in fonts:
            font_name = font[3]
            print(f"Gefundene Schriftart: {font_name}")

# Liste der Bildpfade erhalten (Pfad anpassen)
image_extensions = ['jpg', 'jpeg', 'png', 'dng']
image_paths = [glob.glob(IMAGE_PATHS_PATTERN.format(ext=ext), recursive=True) for ext in image_extensions]
image_paths = [item for sublist in image_paths for item in sublist]

if not image_paths:
    print("Keine Bilder gefunden. Überprüfe den Pfad.")
else:
    print(f"{len(image_paths)} Bilder gefunden.")
    pdfs = create_pdf(image_paths)
    merge_pages_in_pdf_memory(pdfs, output_dir, base_filename)
