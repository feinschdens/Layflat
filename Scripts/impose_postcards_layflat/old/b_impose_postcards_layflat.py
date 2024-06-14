from PIL import Image
from fpdf import FPDF
import os

# Parameter
dateiformat_breite = 155
dateiformat_hoehe = 105
abstand_d = 5
druckbogen_hoehe = 305
druckbogen_breite = 640

# Sicherstellen, dass das Bild im RGB-Modus vorliegt und auf die richtige Größe skaliert wird
def prepare_image(image, width, height):
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image.resize((width, height), Image.LANCZOS)

# Platzierung der Dateien und Speichern als PDF
def platzieren_dateien_und_speichern_als_pdf(druckbogen_breite, druckbogen_hoehe, dateiformat_breite, dateiformat_hoehe, abstand_d, postcard_backprint, client_jpgs, output_path):
    # Erstelle ein leeres Bild für den Druckbogen im Querformat
    druckbogen = Image.new('RGB', (druckbogen_breite, druckbogen_hoehe), 'white')

    # Lade und bereite alle JPG-Dateien aus den Ordnern vor
    dateien_client_jpgs = [prepare_image(Image.open(os.path.join(client_jpgs, file)), dateiformat_breite, dateiformat_hoehe) for file in os.listdir(client_jpgs) if file.endswith('.jpg')]
    dateien_postcard_backprint = [prepare_image(Image.open(os.path.join(postcard_backprint, file)), dateiformat_breite, dateiformat_hoehe) for file in os.listdir(postcard_backprint) if file.endswith('.jpg')]

    # Linker Teil
    for row in range(2):
        for col in range(3):
            index = row * 3 + col
            if index < len(dateien_client_jpgs):
                x = col * (dateiformat_breite + abstand_d)
                y = row * (dateiformat_hoehe + abstand_d)
                druckbogen.paste(dateien_client_jpgs[index], (x, y))

    # Rechter Teil
    for row in range(2):
        for col in range(3):
            index = row * 3 + col
            if index < len(dateien_postcard_backprint):
                x = 320 + col * (dateiformat_breite + abstand_d)
                y = row * (dateiformat_hoehe + abstand_d)
                druckbogen.paste(dateien_postcard_backprint[index], (x, y))

    # Speichern des Druckbogens als temporäre PNG-Datei
    druckbogen_path = 'druckbogen_temp.png'
    druckbogen.save(druckbogen_path)

    # Erstellen und Speichern der PDF-Datei
    pdf = FPDF(orientation='L', unit='mm', format=(druckbogen_breite, druckbogen_hoehe))
    pdf.add_page()
    pdf.image(druckbogen_path, 0, 0, druckbogen_breite, druckbogen_hoehe)
    pdf.output(output_path)

# Beispielaufruf
postcard_backprint = 'C:\\Users\\peter\\Pictures\\impose_postcards\\postcard_backprint'
client_jpgs = 'C:\\Users\\peter\\Pictures\\impose_postcards\\client_jpgs'
output_path = 'C:\\Users\\peter\\Pictures\\impose_postcards\\results\\druckbogen_erster_bogen.pdf'

platzieren_dateien_und_speichern_als_pdf(druckbogen_breite, druckbogen_hoehe, dateiformat_breite, dateiformat_hoehe, abstand_d, postcard_backprint, client_jpgs, output_path)
