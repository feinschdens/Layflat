import fitz
import os
import glob

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

def diagnose_all_pdfs(output_folder):
    for pdf_file in glob.glob(os.path.join(output_folder, "*.pdf")):
        diagnose_pdf(pdf_file)
