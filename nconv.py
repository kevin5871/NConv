import tkinter
import sys 
import os
from tkinter import *
from tkinter import filedialog
from pathlib import Path
import tempfile
from zipfile import ZipFile

# pip install PIL, pytesseract (for image), pdf2image, pyPDF2 (for pdf), epub-conversion, xml_cleaner (for epub)

# for windows, install tesseract-ocr, poppler and make sure they are registeed in PATH

try :
	os.remove('out_text.txt')
except :
	pass
root = Tk()
root.withdraw()

language = "kor"

os.system("cls")
print("NConv - Novel to txt | v 1.0")
print("You are responsible for any incident that occurs after using this program.")
print("-"*20)
print("NConv - 책을 txt로 변환 | v 1.0")
print("이 프로그램을 사용한 후 발생하는 사건에 대하여 모든 책임은 사용자에게 있습니다.")

td = tempfile.TemporaryDirectory()
path = td.name

File = filedialog.askopenfilename(initialdir = "%HOMEPATH%/Downloads",title = "Open file",filetypes = (("pdf files","*.pdf"),("zip files","*.zip"),("epub files","*.epub"),("all files","*.*")))
File_type = str(File).split('/')[-1].split('.')[-1]
filelimit = 0

print("-"*20)

# pdf to image
if File_type == 'pdf' :
	# IMPORT FOR PDF
	from pdf2image import convert_from_path
	import PyPDF2

	reader = PyPDF2.PdfFileReader(File) 
	pages = convert_from_path(File, dpi=300)
	image_counter = 1

	for page in pages:
		print("PDFtoImage Process : %s / %s (%s%%)"% (str(image_counter), str(reader.getNumPages()), str(int(image_counter / reader.getNumPages() * 100))))
		page.save(os.path.join(path, "page_"+str(image_counter)+".jpg"), 'JPEG') 
		image_counter = image_counter + 1
	
	filelimit = image_counter-1

# zip to image (extract)
elif File_type == 'zip' :
	zf = ZipFile(File, 'r')
	zf.extractall(path)
	l = os.listdir(path)
	myimages  = []
	l.sort()
	sorted(l)
	for files in l :
		myimages.append(files)
	image_counter = 1
	for a in myimages :
		if a.split('.')[-1] == 'jpg' :
			os.rename(os.path.join(path, a), os.path.join(path, "page_"+str(image_counter).zfill(5)+".jpg"))
		elif a.split('.')[-1] == 'png' :
			os.rename(os.path.join(path, a), os.path.join(path, "page_"+str(image_counter).zfill(5)+".png"))
		else :
			print("Error : FileTypeNotSupported")
			print("zip 파일 내부에 호환되지 않는 파일이 있습니다. (jpg, png)")
			os.system("pause")
			sys.exit(0)
		image_counter = image_counter + 1
	#print(os.listdir(path))
	filelimit = image_counter-1
	print("ZiptoImg Process : Completed | %d Images Detected." % (filelimit))

# epub to txt
elif File_type == 'epub' :
	"""
	shutil.copyfile(File, os.path.join(path, "file.epub"))
	converter = epub_conversion.Converter(os.path.join(path))
	converter.convert("my_succinct_text_file.gz")
	"""
	from epub_conversion.utils import open_book, convert_epub_to_lines, convert_lines_to_text
	book = open_book(File)
	lines = convert_epub_to_lines(book)
	f = open("out_text.txt", "a", encoding="utf-8") 
	for a in lines :
		f.write(''.join(convert_lines_to_text(a)))
	f.close()
	td.cleanup()
	print("Successfully Converted to txt | Library Used : Tessearct")
	print("-"*20)
	print("txt로 변환이 완료되었습니다. 위 프로그램은 Tesseract를 사용하였습니다.")
	os.system("pause")
	sys.exit(0)

# FileTypeNotSupported
else :
	print("Error : FileTypeNotSupported")
	print('-'*20)
	print("지원되지 않는 파일입니다. (pdf, zip, epub)")
	os.system("pause")
	sys.exit(0)


#IMPORT FOR IMAGE
import PIL.Image
import pytesseract 

# pytesseract settings
if os.path.exists(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe") :
	pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
elif os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe") :
	pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else :
	tkinter.messagebox.showerror("No Tesseract Find in default Path.")
	pytesseract.pytesseract.tesseract_cmd = filedialog.askopenfilename(initialdir = "C:\\Program Files", filetypes = (("tesseract", "*.exe"), ("all files", "*.*")))

# image to text
f = open("out_text.txt", "a", encoding="utf-8") 
for i in range(1, filelimit + 1): 
	print("ImagetoTxt Process : %s / %s (%d%%)"% (str(i), str(filelimit), int(i / filelimit * 100)))
	try :
		text = str(((pytesseract.image_to_string(PIL.Image.open(os.path.join(path,"page_"+str(i).zfill(5)+".jpg")), lang=language))))
	except :
		text = str(((pytesseract.image_to_string(PIL.Image.open(os.path.join(path,"page_"+str(i).zfill(5)+".png")), lang=language))))
	text = text.replace('-\n', '')	 
	f.write(text)

f.close()

td.cleanup()
print("Successfully Converted to txt | Library Used : Tessearct")
print("-"*20)
print("txt로 변환이 완료되었습니다. 위 프로그램은 Tesseract를 사용하였습니다.")
os.system("pause")