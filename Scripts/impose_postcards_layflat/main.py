# main.py

from file_processing import load_images, load_backprint
from quality_check import check_quality
from layout_generator import generate_layouts
from pdf_creator import create_pdf
import config

def main():
    # Laden der Bilddaten
    images = load_images(config.KUNDENDATEN_FOLDER)
    backprint = load_backprint(config.BACKPRINT_FOLDER)

    # Qualitätsprüfung
    if not check_quality(images):
        print("Qualitätsprüfung fehlgeschlagen.")
        return

    # Layout-Generierung
    layouts = generate_layouts(images, backprint)

    # PDF-Erstellung
    create_pdf(layouts, config.OUTPUT_PATH)

    print(f"PDF erfolgreich erstellt und gespeichert unter {config.OUTPUT_PATH}.")

if __name__ == "__main__":
    main()
