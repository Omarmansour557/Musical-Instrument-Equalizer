from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic


class Equalizer (qtw.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("src/ui/equalizer.ui", self)
