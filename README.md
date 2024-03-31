# Compressing Difficult pdfs via

This Python script is designed to compress PDF files containing mainly images by extracting images from each page, compressing the images individually, and then creating a new PDF file with the compressed images.

## Prerequisites

Before running the script, ensure that you have the [ImageMagick](https://imagemagick.org/script/download.php) installed on your system and accessible from the command line.

You can install ImageMagick in Mac through:

```
brew install imagemagick
```
and
```
brew install ghostscript
```

## Usage

1. Place the script file (`compress_pdfs.py`) in the directory where your PDF files are located.

2. Open a terminal in the directory containing the script and PDF files.

3. Run the script using the following command:
   ```
   python compress.py
   ```

4. The script will iterate over all PDF files in the current directory (excluding files ending with `_c.pdf`), compress each PDF file, and save the compressed version with the suffix `_c.pdf`.

Note: The script assumes that the PDF files are located in the same directory as the script file. If your PDF files are in a different directory, modify the script accordingly.

## Disclaimer

Please ensure that you have backups of your PDF files before running this script, as it removes the original PDF files after compression. Use the script at your own risk.
