import sys 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from program import Program
import pathlib

class Main:
    def __init__(self):
        #app = QtWidgets.QApplication(sys.argv)
        gallery = Program()
        gallery.show()
        #sys.exit(app.exec_())
     
