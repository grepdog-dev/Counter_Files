import tkinter.messagebox
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from tkinter import filedialog
from osch import *
import tkinter

class values():
    filder = ""
    filen = ""
    name = ""


Form, Window = uic.loadUiType("design.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def cl_och():
    form.list.clear()

def cl_cat():
    values.filder = filedialog.askdirectory()
    values.filder = f"{values.filder}/"

    values.kolv = len(values.filder)

    if values.filder != "":
        form.lbl_kat.setText(f"Категория : {values.filder}")
        vybkat(values.filder)

    else:
        pass

def cl_fa():
    filen = filedialog.askopenfilename()
    if filen != "":
        values.name = filen[len(values.filder):]
        form.list.addItem(values.name)
        vybfay(values.name)
    else:
        tkinter.messagebox.showwarning("ПРЕДУПРЕЖДЕНИЕ!", "Вы забыли выбрать категорию!")

def zag():
    schet = form.spinBox.value()
    pre(schet)

def jp():
    selected = form.list.currentRow()
    if selected >= 0:
        current_item = form.list.takeItem(selected)
        form.list.insertItem(selected - 1, current_item)

def doen():
    selected = form.list.currentRow()
    if selected >= 0:
        current_item = form.list.takeItem(selected)
        form.list.insertItem(selected + 1, current_item)

def dele():
    current_row = form.list.currentRow()
    if current_row >= 0:
        current_item = form.list.takeItem(current_row)
        del current_item


form.btn_och.clicked.connect(cl_och)
form.btn_fa.clicked.connect(cl_fa)
form.btn_kat.clicked.connect(cl_cat)
form.btn_pre.clicked.connect(zag)
form.btn_up.clicked.connect(jp)
form.btn_down.clicked.connect(doen)
form.btn_del.clicked.connect(dele)

app.exec_()