import tkinter
import sys
import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
import tempfile
from zipfile import ZipFile

root = Tk()
root.withdraw()

File = ''
Output_File = ''
percent = 0
language="kor"

def OpenFile():
    global File, File_type
    File = filedialog.askopenfilename(initialdir="%HOMEPATH%/Downloads", title="Open file", filetypes=(
        ("pdf files", "*.pdf"), ("zip files", "*.zip"), ("epub files", "*.epub"), ("all files", "*.*")))
    File_type = str(File).split('/')[-1].split('.')[-1]


def OpenSaveFile():
    global Output_File
    Output_File = filedialog.asksaveasfilename(
        initialfile="out_text.txt", title="Save File", filetypes=(("txt files", ".txt"), ("all files", "*.*")))
    # print(Output_File)


def FileTypeNotSupported():
    print("Error : FileTypeNotSupported")


def PdfToImage():
    global File, filelimit, path, td, percent, st
    from pdf2image import convert_from_path
    import PyPDF2

    reader = PyPDF2.PdfFileReader(File)
    pages = convert_from_path(File, dpi=300)
    image_counter = 1
    percent = 0
    for page in pages:
        percent = int(image_counter / reader.getNumPages() * 100)
        print("PDFtoImage Process : %s / %s (%d%%)" %
                (str(image_counter), str(reader.getNumPages()), percent))
        page.save(os.path.join(path, "page_"+str(image_counter)+".jpg"), 'JPEG')
        image_counter = image_counter + 1

    filelimit = image_counter-1
    l = os.listdir(path)
    myimages = []
    l.sort()
    sorted(l)
    for files in l:
        myimages.append(files)
    image_counter = 1
    for a in myimages:
        if a.split('.')[-1] == 'jpg':
            os.rename(os.path.join(path, a), os.path.join(
                path, "page_"+str(image_counter).zfill(5)+".jpg"))
        elif a.split('.')[-1] == 'png':
            os.rename(os.path.join(path, a), os.path.join(
                path, "page_"+str(image_counter).zfill(5)+".png"))
        else:
            FileTypeNotSupported()

        image_counter = image_counter + 1
    # print(os.listdir(path))
    filelimit = image_counter-1


def ZipToImage():
    global File, path, filelimit, st
    zf = ZipFile(File, 'r')
    zf.extractall(path)
    l = os.listdir(path)
    myimages = []
    l.sort()
    sorted(l)
    for files in l:
        myimages.append(files)
    image_counter = 1
    for a in myimages:
        if a.split('.')[-1] == 'jpg':
            os.rename(os.path.join(path, a), os.path.join(
                path, "page_"+str(image_counter).zfill(5)+".jpg"))
        elif a.split('.')[-1] == 'png':
            os.rename(os.path.join(path, a), os.path.join(
                path, "page_"+str(image_counter).zfill(5)+".png"))
        else:
            FileTypeNotSupported()

        image_counter = image_counter + 1
    # print(os.listdir(path))
    filelimit = image_counter-1
    print("ZiptoImg Process : Completed | %d Images Detected." % (filelimit))
   


def EpubtoTxt():
    global File
    from epub_conversion.utils import open_book, convert_epub_to_lines, convert_lines_to_text
    book = open_book(File)
    lines = convert_epub_to_lines(book)
    f = open(Output_File, "a", encoding="utf-8")
    for a in lines:
        f.write(''.join(convert_lines_to_text(a)))
    f.close()
    td.cleanup()


def ImagetoTxt():
    global Output_File, td, path, filelimit, language, percent, st

    import PIL.Image
    import pytesseract

    # pytesseract settings
    if os.path.exists(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    elif os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    else:
        tkinter.messagebox.showerror("No Tesseract Find in default Path.")
        pytesseract.pytesseract.tesseract_cmd = filedialog.askopenfilename(
            initialdir="C:\\Program Files", filetypes=(("tesseract", "*.exe"), ("all files", "*.*")))
    percent = 0
    # image to text
    f = open(Output_File, "a", encoding="utf-8")
    for i in range(1, filelimit + 1):
        percent = int(i / filelimit * 100)
        print("ImagetoTxt Process : %s / %s (%d%%)" %
                (str(i), str(filelimit), percent))
        try:
            text = str(((pytesseract.image_to_string(PIL.Image.open(
                os.path.join(path, "page_"+str(i).zfill(5)+".jpg")), lang=language))))
        except:
            text = str(((pytesseract.image_to_string(PIL.Image.open(
                os.path.join(path, "page_"+str(i).zfill(5)+".png")), lang=language))))
        # text = text.replace('-\n', '')

        f.write(text)

    f.close()


def Start():
    global path, filelimit, File_type, td, Output_File, language, percent
    td = tempfile.TemporaryDirectory()
    path = td.name
    filelimit = 0
    if File_type == 'pdf':
        PdfToImage()
        ImagetoTxt()

    elif File_type == 'zip':
        ZipToImage()
        ImagetoTxt()

    elif File_type == 'epub':
        EpubtoTxt()

    else:
        FileTypeNotSupported()

    td.cleanup()


if __name__ == "__main__":
    os.system("cls")
    print("NConv - Novel to txt | v 2.0")
    print("You are responsible for any incident that occurs after using this program.")

    OpenFile()
    OpenSaveFile()

    Start()

    print("Successfully Converted to txt | Library Used : Tessearct")
    os.system("pause")
