import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
import io

def merge_pages_in_pdf(input_folder, output_folder):
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]
    pdf_files.sort()
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for pdf_file in pdf_files:
        print(f"Processing file: {pdf_file}")
        input_path = os.path.join(input_folder, pdf_file)
        doc = fitz.open(input_path)
        writer = PdfWriter()

        output_filename = f"merged_{pdf_file}"
        output_path = os.path.join(output_folder, output_filename)

        # Assuming the pages are squares with 300x300 points
        original_width = 300
        original_height = 300
        merged_width = 2 * original_width

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(merged_width, original_height))
        
        for i in range(0, len(doc), 2):
            print(f"Processing pages {i} and {i + 1} of {pdf_file}")
            if i + 1 < len(doc):
                page1 = doc[i]
                page2 = doc[i + 1]

                pix1 = page1.get_pixmap()
                pix2 = page2.get_pixmap()

                img1_path = f"page1_{i}.png"
                img2_path = f"page2_{i + 1}.png"
                pix1.save(img1_path)
                pix2.save(img2_path)

                # Draw the images side by side
                can.drawImage(img1_path, 0, 0, width=original_width, height=original_height)
                can.drawImage(img2_path, original_width, 0, width=original_width, height=original_height)
            else:
                page1 = doc[i]
                pix1 = page1.get_pixmap()

                img1_path = f"page1_{i}.png"
                pix1.save(img1_path)

                can.drawImage(img1_path, 0, 0, width=original_width, height=original_height)
            
            can.showPage()

        can.save()
        packet.seek(0)

        new_pdf = PdfReader(packet)
        for page in new_pdf.pages:
            writer.add_page(page)

        with open(output_path, 'wb') as output_pdf:
            writer.write(output_pdf)

        print(f"Pages in {pdf_file} merged into {output_path}")

        os.remove(img1_path)
        if i + 1 < len(doc):
            os.remove(img2_path)

input_folder = r'C:\Users\peter\Pictures\Familie'
output_folder = r'C:\Users\peter\Pictures\Familie\merged'

merge_pages_in_pdf(input_folder, output_folder)
