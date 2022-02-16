from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from guitar import Guitar
from piano import Keyboard
from drum import Drum
from equalizer import Equalizer


class Page (qtw.QTabWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("src/ui/page.ui", self)

        self.piano_tab = Keyboard()
        self.guitar_tab = Guitar()
        self.drum_tab = Drum()
        self.equalizer_tab = Equalizer()

        self.DrumLayout.addWidget(self.drum_tab)
        self.PianoLayout.addWidget(self.piano_tab)
        self.GuitarLayout.addWidget(self.guitar_tab)
        self.EqualizerLayout.addWidget(self.equalizer_tab)
