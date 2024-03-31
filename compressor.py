import os
import io
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from multiprocessing import Pool
from tqdm import tqdm

def compress_image(image, quality=20):
    if image.mode == 'P':
        image = image.convert('RGB')
    compressed_img = io.BytesIO()
    image.save(compressed_img, format='JPEG', quality=quality)
    compressed_img.seek(0)
    return compressed_img

def compress_pdf(input_path, output_path):
    try:
        images = convert_from_path(input_path)
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        with Pool() as pool:
            compressed_images = list(pool.imap(compress_image, images))

        for compressed_image in compressed_images:
            img = ImageReader(compressed_image)
            img_width, img_height = img.getSize()
            scale = min(width / img_width, height / img_height)
            scaled_width = img_width * scale
            scaled_height = img_height * scale
            x = (width - scaled_width) / 2
            y = (height - scaled_height) / 2
            c.drawImage(img, x, y, width=scaled_width, height=scaled_height)
            c.showPage()
        c.save()
    except Exception as e:
        print(f"Error compressing {input_path}: {str(e)}")
        raise

def compress_all_pdfs():
    current_dir = os.getcwd()
    pdf_files = [filename for filename in os.listdir(current_dir) if filename.endswith('.pdf') and not filename.endswith('_c.pdf')]

    with tqdm(total=len(pdf_files), unit='file', desc="Compressing PDFs", dynamic_ncols=True) as progress_bar:
        for filename in pdf_files:
            input_path = os.path.join(current_dir, filename)
            output_path = os.path.join(current_dir, f"{os.path.splitext(filename)[0]}_c.pdf")
            try:
                compress_pdf(input_path, output_path)
                os.remove(input_path)
            except Exception as e:
                print(f"Skipping {filename} due to an error: {str(e)}")
            progress_bar.update(1)

if __name__ == '__main__':
    compress_all_pdfs()
