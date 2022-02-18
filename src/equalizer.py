from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import pyqtgraph as pg
from scipy.io import wavfile
import numpy as np
import qtawesome as qta
import sounddevice as sd
from scipy import signal
import matplotlib.pyplot as plt
import math
from equalizer_worker import EqualizerWorker
# import holoviews as hv
# from colorcet.plotting import swatches, sine_combs

# hv.notebook_extension("matplotlib")


def addIcon(name, icon, layout, color):
    icon = qta.IconWidget(icon, color=color)
    icon.setSizePolicy(qtw.QSizePolicy.Policy.Maximum,
                       qtw.QSizePolicy.Policy.Maximum)
    icon.setIconSize(qtc.QSize(32, 32))
    icon.setToolTip(name)
    icon.update()
    layout.addWidget(icon)


class Equalizer (qtw.QWidget):
    sound_signal = qtc.pyqtSignal(object,float,tuple,float)
    def __init__(self):
        super().__init__()

        uic.loadUi("src/ui/equalizer.ui", self)

        self.uiDesigner()

        self.spectrogram_widget = pg.PlotWidget()
        # self.SpectrogramLayout.addWidget(self.spectrogram_widget)

        self.signal_viewer_widget = pg.PlotWidget()
        self.ViewerLayout.addWidget(self.signal_viewer_widget)

        self.LoadButton.clicked.connect(self.openWaveFile)
        self.PlayButton.clicked.connect(self.plotWaveFile)
        self.PauseButton.clicked.connect(self.pauseSound)
        self.SpectrogramRadioBtn.toggled.connect(self.showAndHideSpec)
        self.VolumeSlider.sliderReleased.connect(self.updateGraph)
        
        self.PianoSlider.sliderReleased.connect(self.updatePianoSound)
        self.PiccoloSlider.sliderReleased.connect(self.updatePiccoloSound)
        self.SnareSlider.sliderReleased.connect(self.updateSnareSound)

        self.thread_equalizer = qtc.QThread()

        self.equalizer_worker = EqualizerWorker()

        self.equalizer_worker.moveToThread(self.thread_equalizer)
        self.thread_equalizer.start()

        self.sound_signal.connect(self.equalizer_worker.equalizer)
        self.equalizer_worker.equalizer_ready_now.connect(self.updateDataAfterEqualized)



        pen = pg.mkPen(color=(0, 0, 255))
        self.graph = self.signal_viewer_widget.plot([], [], pen=pen)
        

        self.sample_rate = 0
        self.counter = 0
        self.data = []
        self.raw_data = []
        self.aux_data = []



    def updateDataAfterEqualized(self, data):
        self.aux_data = data
        self.plotSpectrogram()
        sd.play(self.aux_data[self.counter*self.sample_rate//10: ], self.sample_rate)
           
        






    def updatePianoSound(self):
        slider_value_piano = self.PianoSlider.value()
        self.sound_signal.emit(self.data, self.sample_rate, (0,5000), slider_value_piano)


    def updatePiccoloSound(self):
        slider_value_piccolo = self.PiccoloSlider.value()

        self.sound_signal.emit(self.data, self.sample_rate, (5000,10000), slider_value_piccolo)


    def updateSnareSound(self):
        slider_value_snare = self.SnareSlider.value()

        self.sound_signal.emit(self.data, self.sample_rate, (10000,15000), slider_value_snare)





    def uiDesigner(self):
        self.sliders = {"Piano": ["mdi.piano", self.PianoIcon, "green"],
                        "Piccolo": ["ph.magic-wand-thin", self.PiccoloIcon, "red"],
                        "Snare": ["fa5s.drum", self.SnareIcon, "blue"],
                        "Speaker": ["ei.speaker", self.SpeakerIcon, "blue"]}

        for slider_name in self.sliders.keys():
            slider = self.sliders[slider_name]
            addIcon(slider_name, slider[0], slider[1], slider[2])

        self.PlayButton.setIcon(self.style().standardIcon(
            qtw.QStyle.StandardPixmap.SP_MediaPlay))
        self.PauseButton.setIcon(self.style().standardIcon(
            qtw.QStyle.StandardPixmap.SP_MediaStop))

    def openWaveFile(self):
        file_name, b = qtw.QFileDialog.getOpenFileName(
            self, "load file", "", "wav (*.wav)")
        self.sample_rate, self.raw_data = wavfile.read(file_name)

        length = self.raw_data.shape[0] / self.sample_rate
        self.time = np.linspace(0., length, self.raw_data.shape[0])
        self.data = self.raw_data[:, 0]/2**15  # to normalize data
        self.signal_viewer_widget.setYRange(min(self.data), max(self.data))

    def pauseSound(self):
        self.timer.stop()
        sd.stop()

    def plotWaveFile(self):
        self.plotSpectrogram()
        self.timer = qtc.QTimer()
        self.timer.setInterval(1000/10)
        self.timer.timeout.connect(self.framesPerSec)
        self.timer.start()
        sd.play(self.data, self.sample_rate)

        

    def framesPerSec(self):
        if(len(self.aux_data) == 0):
            self.graph.setData(self.time[self.counter*self.sample_rate//10: self.sample_rate*(
                self.counter+1)//10], self.data[self.counter*self.sample_rate//10: self.sample_rate*(self.counter+1)//10])
        else:
            self.graph.setData(self.time[self.counter*self.sample_rate//10: self.sample_rate*(
            self.counter+1)//10], self.aux_data[self.counter*self.sample_rate//10: self.sample_rate*(self.counter+1)//10])



        self.counter += 1

    def plotSpectrogram(self):

        
        self.powerSpectrum, self.freqenciesFound, _, _ = plt.specgram(
            self.data, Fs=self.sample_rate)

        # Interpret image data as row-major instead of col-major
        pg.setConfigOptions(imageAxisOrder='row-major')

        pg.mkQApp()
        self.win = pg.GraphicsLayoutWidget()
        # A plot area (ViewBox + axes) for displaying the image
        p1 = self.win.addPlot()

        # Item for displaying image data
        img = pg.ImageItem()


        




        img.setImage(self.powerSpectrum)
        # Scale the X and Y Axis to time and frequency (standard is pixels)
        img.scale(self.time[-1]/np.size(self.powerSpectrum,
                  axis=1), math.pi/np.size(self.powerSpectrum, axis=0))
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)

        # set colormap
        img.setLookupTable(lut)
        img.setLevels([-50,40])
        p1.addItem(img)
        # Add a histogram with which to control the gradient of the image
        hist = pg.HistogramLUTItem()
        # Link the histogram to the image
        hist.setImageItem(img)
        # If you don't add the histogram to the window, it stays invisible, but I find it useful.
        self.win.addItem(hist)

        hist.gradient.restoreState(
            {'mode': 'rgb',
             'ticks': [(0.5, (0, 182, 188, 255)),
                       (1.0, (246, 111, 0, 255)),
                       (0.0, (75, 0, 113, 255))]})

        # Limit panning/zooming to the spectrogram
        p1.setLimits(xMin=self.time[0], xMax=self.time[-1], yMin=0,
                     yMax=self.powerSpectrum[0][-1])
        # Add labels to the axis
        p1.setLabel('bottom', "Time", units='s')
        # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        p1.setLabel('left', "Frequency", units='Hz')

    def showAndHideSpec(self):
        self.SpectrogramLayout.addWidget(self.win)
        if self.SpectrogramRadioBtn.isChecked():
            self.win.show()
        else:
            self.win.hide()

    def updateGraph(self):
        value = self.VolumeSlider.value()
        self.updateDataAfterChangeSliderVolume(value)


    def updateDataAfterChangeSliderVolume(self, value):
        
        
        factor = 1.2**value
        
        self.aux_data = (self.data) * factor
        sd.play(self.aux_data[self.counter*self.sample_rate//10: ], self.sample_rate)
           
            

        
        

        
