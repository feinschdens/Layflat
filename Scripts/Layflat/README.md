# Imposition Project

## Übersicht
Dieses Projekt erstellt PDFs aus Bildern und führt die Seiten zu einem Layflat-Format zusammen. Es enthält Module zur Bildverarbeitung, PDF-Erstellung und Diagnose von PDFs.

## Dateien
- `config.py`: Konfigurationsdatei zur Steuerung der Pfade und Einstellungen.
- `image_processing.py`: Enthält Funktionen zur Bildverarbeitung.
- `pdf_generation.py`: Enthält Funktionen zur PDF-Erstellung und Zusammenführung.
- `diagnose.py`: Enthält Funktionen zur Diagnose von PDFs.
- `main.py`: Hauptskript zur Ausführung des Programms.
- `README.md`: Diese Datei.

## Konfiguration
Bearbeite die `config.py`, um zwischen statischen Pfaden und Benutzereingaben umzuschalten:

```python
# Umschalten zwischen statischen Pfaden (True) und Benutzereingaben (False)
USE_STATIC_PATHS = True

# Statische Pfade für die Testphase
IMAGE_DIR = r'C:\Users\peter\Pictures\Familie\Test'
OUTPUT_DIR = r'C:\Users\peter\Pictures\Familie\merged'
BASE_FILENAME = 'test'
