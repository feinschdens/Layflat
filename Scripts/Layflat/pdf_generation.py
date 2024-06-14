import os
import io
import glob
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from PyPDF2 import PdfReader, PdfWriter
import fitz
from PIL import Image
from image_processing import correct_orientation, convert_to_rgb, get_scaled_dimensions, get_image_date

# Registriere die TrueType-Schriftart Arial
arial_path = 'C:/Windows/Fonts/arial.ttf'
pdfmetrics.registerFont(TTFont('Arial', arial_path))

# Ersetze Helvetica durch Arial
registerFontFamily('Helvetica', normal='Arial', bold='Arial', italic='Arial', boldItalic='Arial')

# Setze die Standardschriftart auf Arial
def set_standard_font(c):
    c.setFont('Arial', 12)

def create_pdf(image_paths, page_width, page_height, margin, padding, frame_width):
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
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    set_standard_font(c)

    x_start = margin
    y_start = page_height - margin
    x = x_start
    y = y_start

    img_index = 1

    for idx, img_path in enumerate(sorted_image_paths):
        try:
            img = Image.open(img_path)
            img = correct_orientation(img)
            img = convert_to_rgb(img)
            img_width, img_height = get_scaled_dimensions(img, page_width - 2 * margin, page_height - 2 * margin)
            img = img.resize((img_width, img_height), Image.LANCZOS)
        except Exception as e:
            print(f"Fehler beim Öffnen des Bildes {img_path}: {e}")
            continue

        free_space_x = (page_width - img_width) / 2
        free_space_y = (page_height - img_height) / 2

        if x + img_width > page_width - margin:
            x = x_start
            y -= (img_height + padding)

        if y - img_height < margin:
            c.showPage()
            set_standard_font(c)
            x = x_start
            y = y_start
            page_count += 1

            if page_count >= 96:
                c.save()
                packet.seek(0)
                pdfs.append(packet)
                packet = io.BytesIO()
                c = canvas.Canvas(packet, pagesize=(page_width, page_height))
                set_standard_font(c)
                part_number += 1
                page_count = 0

        try:
            img_path_corrected = f"{img_path}_corrected.jpg"
            img.save(img_path_corrected, quality=95)
            c.drawImage(img_path_corrected, x + free_space_x, y - img_height - free_space_y, width=img_width, height=img_height)

            # Setze die Schriftart vor dem Zeichnen des Rahmens
            set_standard_font(c)

            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(frame_width)
            c.rect(x + free_space_x, y - img_height - free_space_y, img_width, img_height)

            os.remove(img_path_corrected)
        except Exception as e:
            print(f"Fehler beim Einfügen des Bildes {img_path} in das PDF: {e}")
            continue

        x += (img_width + padding)
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
        set_standard_font(can)

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
                set_standard_font(can)

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
