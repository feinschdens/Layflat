# quality_check.py

"""
quality_check.py

Modul zur Überprüfung der Bildqualität.
Funktionen:
- check_quality(images): Überprüft, ob alle Bilder die erforderliche Auflösung und den Farbraum haben.
"""

def check_quality(images):
    """
    Überprüft, ob alle Bilder die erforderliche Auflösung und den Farbraum haben.
    Args:
        images (list): Liste der Bilder.
    Returns:
        bool: True, wenn alle Bilder die Qualitätsanforderungen erfüllen, sonst False.
    """
    for img in images:
        if img.info.get('dpi', (0, 0))[0] < 300 or img.info.get('dpi', (0, 0))[1] < 300:
            return False
    return True
