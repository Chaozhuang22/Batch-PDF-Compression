import os
import tempfile
from PIL import Image
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import subprocess
from tqdm import tqdm

def compress_image(image_path, quality=20):
    # Compress the image using ImageMagick
    compressed_path = f"compressed_{os.path.basename(image_path)}"
    subprocess.call(['convert', image_path, '-quality', str(quality), compressed_path])
    return compressed_path

def compress_pdf(input_path, output_path):
    try:
        # Create a temporary directory for extracted images
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract images from the PDF
            images = convert_from_path(input_path, output_folder=temp_dir)

            # Compress individual images
            compressed_images = []
            for i, image in enumerate(images):
                image_path = os.path.join(temp_dir, f"page_{i}.jpg")
                with open(image_path, 'wb') as f:
                    image.save(f, "JPEG")
                compressed_path = compress_image(image_path)
                compressed_images.append(compressed_path)

            # Create a new PDF from compressed images
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            for compressed_image in compressed_images:
                with Image.open(compressed_image) as img:
                    img_width, img_height = img.size
                    scale = min(width / img_width, height / img_height)
                    scaled_width = img_width * scale
                    scaled_height = img_height * scale
                    x = (width - scaled_width) / 2
                    y = (height - scaled_height) / 2
                    c.drawImage(compressed_image, x, y, width=scaled_width, height=scaled_height)
                c.showPage()
            c.save()

            # Clean up temporary files
            for compressed_image in compressed_images:
                os.remove(compressed_image)
    except Exception as e:
        print(f"Error compressing {input_path}: {str(e)}")

def compress_all_pdfs():
    # Get the current directory
    current_dir = os.getcwd()

    # Get a list of all PDF files in the current directory
    pdf_files = [filename for filename in os.listdir(current_dir) if filename.endswith('.pdf')]

    # Filter out files that end with _c.pdf
    pdf_files = [filename for filename in pdf_files if not filename.endswith('_c.pdf')]

    # Create a progress bar
    progress_bar = tqdm(total=len(pdf_files), unit='file')

    # Iterate over the PDF files
    for filename in pdf_files:
        input_path = os.path.join(current_dir, filename)
        output_path = os.path.join(current_dir, f"{os.path.splitext(filename)[0]}_c.pdf")
        compress_pdf(input_path, output_path)
        print(f"Compressed: {filename}")

        # Remove the original PDF file
        os.remove(input_path)
        print(f"Removed: {filename}")

        # Update the progress bar
        progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()

# Usage
compress_all_pdfs()
