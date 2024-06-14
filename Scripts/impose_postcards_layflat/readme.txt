# Postkarten Druckbogen Generator

Dieses Programm erstellt Druckbögen für Postkarten aus Kundendaten und einer Rückseitendatei. Die Druckbögen werden im Layflat-Bindverfahren erstellt und als PDF gespeichert.

## Funktionen

- **Dateiverarbeitung**: Laden der Bilder aus den Ordnern "Kundendaten" und "Backprint".
- **Qualitätsprüfung**: Überprüfung der Bildauflösung (300 ppi) und des Farbraums (sRGB).
- **Layout-Generierung**: Bestimmung der optimalen Rastergröße (2x3, 3x2 oder 3x3) und Platzierung der Bilder.
- **PDF-Erstellung**: Erstellung und Speicherung der Druckbögen als PDF.

## Voraussetzungen

- Python 3.x
- Pillow (Python Imaging Library)
- fpdf (Python PDF Library)

Installiere die benötigten Bibliotheken mit:

```bash
pip install pillow fpdf
