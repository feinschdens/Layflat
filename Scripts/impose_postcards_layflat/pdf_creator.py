# pdf_creator.py

"""
pdf_creator.py

Modul zur Erstellung und Speicherung der Druckbögen als PDF.
Funktionen:
- create_pdf(layouts, output_path): Erstellt und speichert die Druckbögen als PDF an einem angegebenen Speicherort.
"""

from fpdf import FPDF
import os

def create_pdf(layouts, output_path):
    """
    Erstellt und speichert die Druckbögen als PDF.
    Args:
        layouts (list): Liste der generierten Layouts.
        output_path (str): Speicherpfad für die Ausgabe-PDF.
    """
    pdf = FPDF()
    for layout in layouts:
        pdf.add_page()
        # layout.save("temp_layout.jpg")  # Temporäre Datei speichern, um sie in die PDF einzufügen
        pdf.image(layout, x=0, y=0, w=layout.width, h=layout.height)
    
    # Überprüfen, ob der Ausgabeordner existiert, und gegebenenfalls erstellen
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pdf.output(output_path)
