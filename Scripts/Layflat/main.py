import os
import glob
from tkinter import simpledialog, Tk, filedialog
from config import USE_STATIC_PATHS, IMAGE_DIR, OUTPUT_DIR, BASE_FILENAME
from image_processing import correct_orientation, convert_to_rgb, get_scaled_dimensions, get_image_date
from pdf_generation import create_pdf, merge_pages_in_pdf_memory
from diagnose import diagnose_all_pdfs
from reportlab.lib.pagesizes import mm

def main():
    root = Tk()
    root.withdraw()  # Hauptfenster ausblenden

    if USE_STATIC_PATHS:
        image_dir = IMAGE_DIR
        output_dir = OUTPUT_DIR
        base_filename = BASE_FILENAME
    else:
        # Verzeichnisse auswählen
        image_dir = filedialog.askdirectory(title="Wählen Sie das Verzeichnis mit den Bildern")
        output_dir = filedialog.askdirectory(title="Wählen Sie das Verzeichnis für die zusammengeführten PDFs")
        
        if not image_dir or not output_dir:
            print("Verzeichnisse wurden nicht korrekt ausgewählt.")
            return

        base_filename = simpledialog.askstring("Dateiname", "Wie soll die gespeicherte Datei lauten?")
        if not base_filename:
            print("Kein Dateiname angegeben.")
            return

    PAGE_WIDTH = 300 * mm
    PAGE_HEIGHT = 300 * mm
    MARGIN = 20 * mm
    PADDING = 5 * mm
    FRAME_WIDTH = 0.3 * mm

    IMAGE_PATHS_PATTERN = os.path.join(image_dir, '**', '*.{ext}')
    image_extensions = ['jpg', 'jpeg', 'png', 'dng']
    image_paths = [glob.glob(IMAGE_PATHS_PATTERN.format(ext=ext), recursive=True) for ext in image_extensions]
    image_paths = [item for sublist in image_paths for item in sublist]

    if not image_paths:
        print("Keine Bilder gefunden. Überprüfe den Pfad.")
    else:
        print(f"{len(image_paths)} Bilder gefunden.")
        pdfs = create_pdf(image_paths, PAGE_WIDTH, PAGE_HEIGHT, MARGIN, PADDING, FRAME_WIDTH)
        merge_pages_in_pdf_memory(pdfs, output_dir, base_filename)
        diagnose_all_pdfs(output_dir)

if __name__ == "__main__":
    main()
