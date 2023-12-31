# PDF Resume

Itera en los PDFs para sacar un Screenshot y pegarlos en un reporte mensual junto con su link.

## Instalación

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### Requisitos

Asegúrate de tener instalados los siguientes requisitos:

- Python 3.x: [Descargar e Instalar Python](https://www.python.org/downloads/)

### Pasos de Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/safernandez666/PDFResume.git

2. Instala las dependencias: 

   ```bash
   pip3 install -r requirements.txt

3. Rellena con los link, de los PDF, en el archivo /urls/urls.txt 

4. Generar un Token en [TinyURL](https://tinyurl.com/), para acortar las URLs en el reporte. El mismo debe cargarse en .env

   ```bash
   TOKEN=TUTOKEN

5. Corre el programa:

   ```bash
   python3 main.py

6. Revisar los reportes, generados, en /reports/MES_capturas.pdf
