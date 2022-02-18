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


class EqualizerWorker(qtc.QObject):

    equalizer_ready_now = qtc.pyqtSignal(object)

    @qtc.pyqtSlot(object, float, tuple, float)
    def equalizer(self, data, fs, fre_range, factor):

        amp = np.fft.rfft(data)
        freq = np.fft.rfftfreq(len(data), 1 / fs)
        for i, f in enumerate(freq):

            if f > fre_range[0] and f < fre_range[1]:  # (1)
                amp[i] *= 1.15**factor

        data_after_change = (np.fft.irfft(amp))
        self.equalizer_ready_now.emit(data_after_change)
