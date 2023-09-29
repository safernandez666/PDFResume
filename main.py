import os, shutil
import requests
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image as PILImage
from fpdf import FPDF
from datetime import datetime
from pyshorteners import Shortener
from decouple import config

TOKEN = config('TOKEN')

def shorten_url_with_tinyurl(long_url):
    shortener = Shortener()
    return shortener.tinyurl.short(long_url)

def delete_files():
    # Verifica si el archivo "urls/urls_path.txt" existe antes de intentar eliminarlo
    urls_file = "urls/urls_path.txt"
    if os.path.exists(urls_file):
        os.remove(urls_file)
        print(f"El archivo {urls_file} ha sido eliminado.")
    else:
        print(f"El archivo {urls_file} no existe.")
    
    # Verifica si la carpeta "pdfs" existe antes de intentar eliminarla
    pdfs_folder = "pdfs"
    if os.path.exists(pdfs_folder):
        shutil.rmtree(pdfs_folder)
        print(f"La carpeta {pdfs_folder} y su contenido han sido eliminados.")
    else:
        print(f"La carpeta {pdfs_folder} no existe.")
    
    # Verifica si la carpeta "snapshots" existe antes de intentar eliminarla
    snapshots_folder = "snapshots"
    if os.path.exists(snapshots_folder):
        shutil.rmtree(snapshots_folder)
        print(f"La carpeta {snapshots_folder} y su contenido han sido eliminados.")
    else:
        print(f"La carpeta {snapshots_folder} no existe.")

def convert_pdfs_to_images():
    # Nombre del archivo que contiene las URL y rutas de los PDFs
    url_path_file = "urls/urls_path.txt"
    # Carpeta donde quieres guardar las capturas
    snapshot_folder = "snapshots"
    os.makedirs(snapshot_folder, exist_ok=True)

    # Leer todas las líneas del archivo url_path_file
    with open(url_path_file, "r") as file:
        lines = file.readlines()

    # Crear una lista para almacenar las líneas actualizadas
    updated_lines = []

    for line in lines:
        line = line.strip()  # Elimina espacios y saltos de línea al principio y al final de la línea
        pdf_url, pdf_path = line.split(" ; ")  # Divide la línea en URL y ruta del PDF
        print(pdf_path)
        # Comprueba si el archivo PDF existe antes de intentar convertirlo
        if os.path.exists(pdf_path):
            # Convierte el PDF en una imagen (captura de la primera página)
            images = convert_from_path(pdf_path, first_page=0, last_page=1)

        if images:
            # Genera la ruta para la imagen PNG en la carpeta "snapshots"
            image_path = os.path.join(snapshot_folder, os.path.basename(pdf_path).replace(".pdf", ".png"))

            # Guarda la primera página como un archivo PNG en la carpeta "snapshots"
            images[0].save(image_path, "PNG")

            # Agrega la ruta del snapshot a la línea actual
            line = f"{pdf_url} ; {pdf_path} ; {image_path}\n"

            print(f"Imagen guardada para {pdf_path} como {image_path}")
        else:
            print(f"El PDF {pdf_path} no existe.")

        # Agregar la línea actualizada a la lista
        updated_lines.append(line)

    # Reemplazar el contenido del archivo "urls_path.txt" con las líneas actualizadas
    with open(url_path_file, "w") as url_path:
        url_path.writelines(updated_lines)
        
def download_pdfs_from_urls(txt_file):
    # Carpeta que contiene los PDFs
    pdf_folder = "pdfs"
    os.makedirs(pdf_folder, exist_ok=True)
    # Ruta completa al archivo que contendrá las URL y rutas de los PDFs descargados
    url_path_file = os.path.join("urls", "urls_path.txt")

    with open(txt_file, "r") as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()  # Elimina espacios y saltos de línea al principio y al final de la URL
        response = requests.get(url)
        
        if response.status_code == 200:
            # Obtiene el nombre del archivo desde la URL
            filename = os.path.join(pdf_folder, os.path.basename(url))
            
            # Guarda el PDF en la carpeta "pdfs"
            with open(filename, "wb") as pdf_file:
                pdf_file.write(response.content)
            
            print(f"Se ha descargado y guardado el PDF desde {url} como {filename}")

            # Agrega la URL y la ruta del PDF al archivo "url_path.txt" en la carpeta "urls"
            with open(url_path_file, "a") as url_path:
                url_path.write(f"{url} ; {filename}\n")
        else:
            print(f"No se pudo descargar el PDF desde {url}")

def create_report():
    # Obtén el nombre del mes actual
    current_month = datetime.now().strftime("%B")

    # Nombre del archivo PDF de salida con el nombre del mes y ubicación en la carpeta "reports"
    output_folder = "reports"
    os.makedirs(output_folder, exist_ok=True)
    output_pdf = os.path.join(output_folder, f"{current_month}_capturas.pdf")

    # Abre el file "urls_path.txt" en la subcarpeta "urls" para leer las rutas de las imágenes y los enlaces
    with open("urls/urls_path.txt", "r") as file:
        lines = file.readlines()

    # Crea el PDF combinando las imágenes y los enlaces
    c = canvas.Canvas(output_pdf, pagesize=letter)

    for line in lines:
        parts = line.strip().split(" ; ")
        if len(parts) == 3:
            link = shorten_url_with_tinyurl(parts[0])  # Segunda posición contiene el enlace
            image_path = parts[2]  # Tercera posición contiene la ruta de la imagen
            if os.path.exists(image_path) and image_path.endswith(".png"):
                c.setFont("Helvetica", 12)
                c.drawString(10, 750, f"Enlace: {link}")
                c.drawImage(image_path, 10, 100, width=letter[0] - 20, height=650)
                c.showPage()

    c.save()

    print(f"Se ha creado el archivo PDF combinado como {output_pdf} en la carpeta 'reports'.")

# Limpieza de Carpetas y Archivos Temporales
delete_files()
# Llama a la función y proporciona la ruta completa al archivo TXT en la carpeta "urls"
download_pdfs_from_urls(os.path.join("urls", "urls.txt"))
convert_pdfs_to_images()
create_report()
