import os
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def convert_pdf_to_image():
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)

            # Convierte el PDF en una imagen (captura de la primera página)
            images = convert_from_path(pdf_path, first_page=0, last_page=1)

            if images:
                # Guarda la primera página como un archivo PNG en la carpeta de capturas
                snapshot_path = os.path.join(snapshot_folder, f"{os.path.splitext(filename)[0]}.png")
                images[0].save(snapshot_path, "PNG")

                print(f"Captura guardada para {filename} como {snapshot_path}")
    print("Todas las capturas se han creado exitosamente!")

def combine_images_to_pdf():
    # Carpeta donde están las imágenes
    snapshot_folder = "snapshots"
    
    # Obtiene el nombre del mes actual
    current_month = datetime.now().strftime("%B")
    
    # Nombre del archivo PDF de salida con el nombre del mes
    output_pdf = f"{current_month}_capturas.pdf"
    
    # Lista de rutas de las imágenes
    image_paths = []
    
    # Recorre la carpeta y agrega las imágenes a la lista
    for filename in os.listdir(snapshot_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(snapshot_folder, filename)
            image_paths.append(image_path)
    
    # Crea el PDF combinando las imágenes
    c = canvas.Canvas(output_pdf, pagesize=letter)
    
    for img_path in image_paths:
        c.drawImage(img_path, 0, 0, width=letter[0], height=letter[1])
        c.showPage()
    
    c.save()
    
    print(f"Se ha creado el archivo PDF combinado como {output_pdf}")

# Carpeta que contiene los PDFs
pdf_folder = "pdfs"
os.makedirs(pdf_folder, exist_ok=True)
# Carpeta donde quieres guardar las capturas
snapshot_folder = "snapshots"
os.makedirs(snapshot_folder, exist_ok=True)

# Itera a través de los archivos PDF en la carpeta
convert_pdf_to_image()
# Llama a la función para combinar las imágenes en un PDF
combine_images_to_pdf()

