# NConv - Convert PDF / ZIP / EPUB to TXT
* This project is only tested in `Windows`

## Usage
1. Start `nconv.py`
2. Open Files
3. Wait for Finish
4. `out_text.txt` is what you are waiting for.

## Requires
 * For `Image` :
 `pip install PIL`
 `pip install pytesseract`
 * For `PDF` :
 `pip install pdf2image`
 `pip install pyPDF2`
 * For `EPUB` :
 `pip install epub-conversion`
 `pip install xml_cleaner`
 
 * for windows, install tesseract-ocr, <b>poppler</b> and make sure they are registeed in PATH
 
## Details
* `PDF` and `ZIP` files are read by `tesseract-ocr`
* only images are allowed in `ZIP` files.
