import tkinter
import sys
import os
from tkinter import *
from tkinter import filedialog
from pathlib import Path
import tempfile
from zipfile import ZipFile
from PyQt5 import QtWidgets, QtGui, QtCore
#from fbs_runtime.application_context.PyQt5 import ApplicationContext

root = Tk()
root.withdraw()

File = ''
Output_File = ''
percent = 0
language = "kor"

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
    if md == 0:
        print("Error : FileTypeNotSupported")
    else:
        ui.textBrowser.append("Error : FileTypeNotSupported")


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
        if md == 0:
            print("PDFtoImage Process : %s / %s (%d%%)" %
                  (str(image_counter), str(reader.getNumPages()), percent))
        else:
            ui.textBrowser.append("[INFO] PDFtoImage Process : %s / %s (%d%%)" %
                                  (str(image_counter), str(reader.getNumPages()), percent))
            ui.progressBar.setValue(percent)
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
    if md == 0:
        print("ZiptoImg Process : Completed | %d Images Detected." % (filelimit))
    else:
        ui.textBrowser.append(
            "[INFO] ZiptoImg Process : Completed | %d Images Detected." % (filelimit))


def EpubtoTxt():
    global File
    from epub_conversion.utils import open_book, convert_epub_to_lines, convert_lines_to_text
    book = open_book(File)
    lines = convert_epub_to_lines(book)
    f = open(Output_File, "a", encoding="utf-8")
    for a in lines:
        f.write(''.join(convert_lines_to_text(a)))
    if md != 0 :
        ui.progressBar.setValue(100)
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
    if md != 0 :
        ui.textBrowser.append("[WARNING] Please be patient - It's Still Working.")
    f = open(Output_File, "a", encoding="utf-8")
    for i in range(1, filelimit + 1):
        #appctxt.app.processEvents()
        app.processEvents()
        percent = int(i / filelimit * 100)
        if md == 0:
            print("ImagetoTxt Process : %s / %s (%d%%)" %
                  (str(i), str(filelimit), percent))
        else:
            ui.textBrowser.append(
                "[INFO] ImagetoTxt Process : %s / %s (%d%%)" % (str(i), str(filelimit), percent))
            ui.progressBar.setValue(percent)
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

# IMPORT FOR IMAGE


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setGeometry(QtCore.QRect(20, 10, 156, 52))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Cond Med")
        font.setPointSize(23)
        self.Title.setFont(font)
        self.Title.setLocale(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Title.setTextFormat(QtCore.Qt.AutoText)
        self.Title.setScaledContents(False)
        self.Title.setObjectName("Title")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 540, 741, 21))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Cond Med")
        font.setPointSize(10)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 220, 431, 301))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(30, 90, 631, 31))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 70, 64, 15))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Cond Med")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.Log = QtWidgets.QLabel(self.centralwidget)
        self.Log.setGeometry(QtCore.QRect(30, 200, 64, 21))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Cond Med")
        font.setPointSize(10)
        self.Log.setFont(font)
        self.Log.setObjectName("Log")
        self.FileBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.FileBrowse.setGeometry(QtCore.QRect(680, 90, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Cond Med")
        font.setPointSize(9)
        self.FileBrowse.setFont(font)
        self.FileBrowse.setObjectName("FileBrowse")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 480, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Cond Med")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 140, 64, 15))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Cond Med")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(30, 160, 631, 31))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.FileBrowse_2 = QtWidgets.QPushButton(self.centralwidget)
        self.FileBrowse_2.setGeometry(QtCore.QRect(680, 160, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Noto Sans Cond Med")
        font.setPointSize(9)
        self.FileBrowse_2.setFont(font)
        self.FileBrowse_2.setObjectName("FileBrowse_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NConvGUI"))
        self.Title.setText(_translate("MainWindow", "NConvGUI"))
        self.label.setText(_translate("MainWindow", "File"))
        self.Log.setText(_translate("MainWindow", "Log"))
        self.FileBrowse.setText(_translate("MainWindow", "Browse..."))
        self.pushButton.setText(_translate("MainWindow", "Start!!"))
        self.label_2.setText(_translate("MainWindow", "Output"))
        self.FileBrowse_2.setText(_translate("MainWindow", "Browse..."))


def FB():
    global File
    OpenFile()
    if File != '':
        ui.textBrowser_2.setText(str(os.path.abspath(File)) if len(
            str(os.path.abspath(File))) <= 60 else str(os.path.abspath(File))[:57]+"...")
    else:
        pass


def OFB():
    global Output_File
    OpenSaveFile()
    if Output_File != '':
        ui.textBrowser_3.setText(str(os.path.abspath(Output_File)) if len(str(
            os.path.abspath(Output_File))) <= 60 else str(os.path.abspath(Output_File))[:57]+"...")
    else:
        pass


def ST():
    if File != '' and Output_File != '':
        ui.textBrowser.append('[Start] Start!!')
        ui.pushButton.setEnabled(False)
        Start()
        End()
    else:
        ui.textBrowser.append('[Error] Please Set the files.')


def End():
    ui.textBrowser.append(
        "Successfully Converted to txt | Library Used : Tessearct")
    ui.pushButton.setEnabled(True)

if __name__ == "__main__":
    #appctxt = ApplicationContext()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.FileBrowse.clicked.connect(FB)
    ui.FileBrowse_2.clicked.connect(OFB)
    ui.pushButton.clicked.connect(ST)
    md = 1

    ui.textBrowser.append("NConv - Novel to txt | v 2.0")
    ui.textBrowser.append(
        "You are responsible for any incident that occurs after using this program.")
    
   # sys.exit(appctxt.app.exec_())
    sys.exit(app.exec_())
