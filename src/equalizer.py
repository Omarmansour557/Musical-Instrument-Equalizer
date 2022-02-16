from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import pyqtgraph as pg
from scipy.io import wavfile
import numpy as np
import qtawesome as qta

def addIcon(name, icon, layout, color):
    icon = qta.IconWidget(icon, color=color)
    icon.setSizePolicy(qtw.QSizePolicy.Policy.Maximum, qtw.QSizePolicy.Policy.Maximum)
    icon.setIconSize(qtc.QSize(32, 32))
    icon.setToolTip(name)
    icon.update()
    layout.addWidget(icon)

class Equalizer (qtw.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("src/ui/equalizer.ui", self)
        self.sliders = {"Piano": [ "mdi.piano", self.PianoIcon, "green"],
                        "Piccolo": [ "ph.magic-wand-thin", self.PiccoloIcon, "red"],
                        "Snare": [ "fa5s.drum", self.SnareIcon, "blue"]}

        for slider_name in self.sliders.keys():
            slider = self.sliders[slider_name]
            addIcon(slider_name, slider[0], slider[1], slider[2])


        self.spectrogram_widget = pg.PlotWidget()
        self.SpectrogramLayout.addWidget(self.spectrogram_widget)

        self.signal_viewer_widget = pg.PlotWidget()
        self.ViewerLayout.addWidget(self.signal_viewer_widget)

        self.PlayButton.setIcon(self.style().standardIcon(qtw.QStyle.StandardPixmap.SP_MediaPlay))
        self.PauseButton.setIcon(self.style().standardIcon(qtw.QStyle.StandardPixmap.SP_MediaStop))


        self.LoadButton.clicked.connect(self.readWaveFile)

    def readWaveFile(widget):
        file_name, b = qtw.QFileDialog.getOpenFileName(widget, "load file", "", "wav (*.wav)")
        sample_rate, data = wavfile.read(file_name)
        print(data.shape[1])
        length = data.shape[0] / sample_rate
        print(f"length = {length}s")
        return sample_rate, data
        
    def plotWavefile(self):
        sample_rate, data = self.readWaveFile(self.spectrogram_widget)
        length = data.shape[0] / sample_rate
        time = np.linspace(0., length, data.shape[0])
        self.signal_viewer_widget.plot(time, data[:, 0])





