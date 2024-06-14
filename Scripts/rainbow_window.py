import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Konfiguration der Audioaufnahme
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 256  # Anzahl der Frames pro Buffer (noch kleinere CHUNK-Größe)
DURATION = 3  # Dauer der Messung in Sekunden

# Funktion zur Berechnung der Frequenzbänder
def calculate_frequencies(signal, rate):
    n = len(signal)
    frequencies = np.fft.fftfreq(n, d=1/rate)
    magnitudes = abs(np.fft.fft(signal))
    return frequencies[:n//2], magnitudes[:n//2]

# Funktion zur Aktualisierung der Visualisierung
def update_plot(frame):
    try:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.float32)
        frequencies, magnitudes = calculate_frequencies(data, RATE)
        line.set_ydata(magnitudes)
        return line,
    except Exception as e:
        print("Error reading audio stream:", e)
        return None

# Initialisierung der PyAudio-Aufnahme
p = pyaudio.PyAudio()
try:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Audio stream opened successfully.")
except Exception as e:
    print("Error opening audio stream:", e)
    stream = None

# Initialisierung der Visualisierung
fig, ax = plt.subplots()
x = np.linspace(0, RATE/2, CHUNK//2)
line, = ax.plot(x, np.random.rand(CHUNK//2))
ax.set_ylim(0, 0.5)
ax.set_xlim(0, RATE/2)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude')
plt.ion()

# Starten der Echtzeit-Visualisierung
if stream:
    ani = FuncAnimation(fig, update_plot, blit=True)
    plt.show()

    # Aufnahme für DURATION Sekunden
    stream.start_stream()
    try:
        while stream.is_active():
            pass
    except KeyboardInterrupt:
        stream.stop_stream()
    stream.close()
    print("Audio stream closed.")
else:
    print("No audio stream available. Exiting.")
p.terminate()
