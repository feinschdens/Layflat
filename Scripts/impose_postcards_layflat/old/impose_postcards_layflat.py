from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def create_layflat_pdf(output_filename, page_width, page_height, num_pages, sheet_width, sheet_height):
    # Convert page and sheet dimensions to millimeters
    page_width_mm = page_width * mm
    page_height_mm = page_height * mm
    sheet_width_mm = sheet_width * mm
    sheet_height_mm = sheet_height * mm

    # Create a Canvas object with the dimensions of the sheet
    c = canvas.Canvas(output_filename, pagesize=(sheet_width_mm, sheet_height_mm))
    
    # Calculate how many pages fit in a row and column on the sheet
    pages_per_row = sheet_width // page_width
    pages_per_col = sheet_height // page_height
    
    # Initialize the page counter
    current_page = 0
    
    # While there are still pages left to draw
    while current_page < num_pages:
        for row in range(pages_per_col):
            for col in range(pages_per_row):
                if current_page < num_pages:
                    # Calculate the position of the page on the sheet
                    x = col * page_width_mm
                    y = sheet_height_mm - (row + 1) * page_height_mm
                    # Draw a rectangle for the page
                    c.rect(x, y, page_width_mm, page_height_mm)
                    # Add the page number
                    c.drawString(x + 5 * mm, y + 5 * mm, f"Page {current_page + 1}")
                    # Increment the page counter
                    current_page += 1
        # Create a new page in the PDF to layout additional pages
        c.showPage()
    
    # Save the PDF
    c.save()

def main():
    # Your values
    output_filename = "layflat_book.pdf"
    page_width = 100  # in mm, 10 cm
    page_height = 150  # in mm, 15 cm
    num_pages = 31
    sheet_width = 635  # in mm, sheet width
    sheet_height = 305  # in mm, sheet height
    
    # Create the PDF
    create_layflat_pdf(output_filename, page_width, page_height, num_pages, sheet_width, sheet_height)

if __name__ == "__main__":
    main()
