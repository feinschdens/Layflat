# file_processing.py

"""
file_processing.py

Modul zur Verarbeitung und Laden von Bilddateien aus den Ordnern "Kundendaten" und "Backprint".
Funktionen:
- load_images(folder): Lädt JPG-Bilder aus dem angegebenen Ordner.
- load_backprint(folder): Lädt die Rückseitendatei (JPG oder PDF) aus dem angegebenen Ordner.
"""

import os
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_images(folder):
    """
    Lädt JPG-Bilder aus dem angegebenen Ordner.
    Args:
        folder (str): Pfad zum Ordner mit den Bildern.
    Returns:
        list: Liste der geladenen Bilder.
    """
    images = []
    try:
        for filename in os.listdir(folder):
            if filename.endswith(".jpg"):
                img = Image.open(os.path.join(folder, filename))
                images.append(img)
        logging.info(f"{len(images)} Bilder erfolgreich aus {folder} geladen.")
    except Exception as e:
        logging.error(f"Fehler beim Laden der Bilder aus {folder}: {e}")
    return images

def load_backprint(folder):
    """
    Lädt die Rückseitendatei (JPG oder PDF) aus dem angegebenen Ordner.
    Args:
        folder (str): Pfad zum Ordner mit der Rückseitendatei.
    Returns:
        Image: Geladene Rückseitendatei.
    """
    try:
        for filename in os.listdir(folder):
            if filename.endswith(".jpg") or filename.endswith(".pdf"):
                logging.info(f"Rückseitendatei {filename} erfolgreich aus {folder} geladen.")
                return Image.open(os.path.join(folder, filename))
    except Exception as e:
        logging.error(f"Fehler beim Laden der Rückseitendatei aus {folder}: {e}")
    return None
