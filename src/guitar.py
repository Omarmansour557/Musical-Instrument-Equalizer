from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import sounddevice as sd
import numpy as np


class Guitar (qtw.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("src/ui/guitar.ui", self)
        self.button_E1 = self.E1  # Find the button
        self.button_A = self.A  # Find the button
        self.button_D = self.D  # Find the button
        self.button_G = self.G  # Find the button
        self.button_B = self.B  # Find the button
        self.button_E2 = self.E2  # Find the button

        self.guitar_buttons = [self.button_E1, self.button_A, self.button_D, self.button_G, self.button_B,
                               self.button_E2]
        self.tones = {"E1": 82, "A": 110, "D": 147,
                      "G": 196, "B": 247, "E2": 330}
        self.guitar_func = [lambda: self.play(self.tones["E1"]), lambda: self.play(self.tones["A"]),
                            lambda: self.play(self.tones["D"]), lambda: self.play(
                                self.tones["G"]),
                            lambda: self.play(self.tones["B"]), lambda: self.play(self.tones["E2"])]

        for i in range(len(self.guitar_buttons)):
            self.guitar_buttons[i].clicked.connect(self.guitar_func[i])

    def karplus_strong(self, wavetable, n_samples):
        """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging."""
        samples = []
        current_sample = 0
        previous_value = 0
        while len(samples) < n_samples:
            wavetable[current_sample] = 0.5 * \
                (wavetable[current_sample] + previous_value)
            samples.append(wavetable[current_sample])
            previous_value = samples[-1]
            current_sample += 1
            current_sample = current_sample % wavetable.size
        return np.array(samples)

    def play(self, freq):
        fs = 30000
        wavetable_size = fs // freq

        wavetable = (2 * np.random.randint(0, 2,
                     wavetable_size) - 1).astype(np.float64)
        sample1 = self.karplus_strong(wavetable, 2 * fs)
        sd.play(sample1, fs)
