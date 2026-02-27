import numpy as np
import sounddevice as sd
import threading


class AudioEngine:
    """Generates a 40Hz amplitude-modulated tone on a configurable carrier wave."""

    def __init__(self):
        self._lock = threading.Lock()
        self._stream = None
        self._phase_idx = 0
        self._running = False

        # Audio parameters (can be changed while running)
        self.carrier_freq = 250.0
        self.mod_freq = 40.0
        self.mod_depth = 1.0
        self.amplitude = 0.3

        # Auto-detect sample rate from default output device
        dev_info = sd.query_devices(sd.default.device[1], 'output')
        self.sample_rate = int(dev_info['default_samplerate'])

    def _audio_callback(self, outdata, frames, time_info, status):
        """Called by sounddevice in a separate high-priority thread."""
        with self._lock:
            carrier_freq = self.carrier_freq
            mod_freq = self.mod_freq
            mod_depth = self.mod_depth
            amplitude = self.amplitude
            sr = self.sample_rate
            idx = self._phase_idx

        t = (idx + np.arange(frames)) / sr
        carrier = np.sin(2.0 * np.pi * carrier_freq * t)
        modulator = 1.0 + mod_depth * np.sin(2.0 * np.pi * mod_freq * t)
        signal = amplitude * carrier * modulator
        outdata[:, 0] = signal.astype(np.float32)

        with self._lock:
            self._phase_idx += frames

    def get_modulation_phase(self):
        """Returns the current 40Hz modulation phase (0.0 to 1.0).

        Flash should be ON when phase < 0.5 (modulator is in positive half).
        """
        with self._lock:
            idx = self._phase_idx
            sr = self.sample_rate
            mod_freq = self.mod_freq
        current_time = idx / sr
        return (current_time * mod_freq) % 1.0

    def start(self):
        if self._running:
            return
        with self._lock:
            self._phase_idx = 0
        self._stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32',
            callback=self._audio_callback,
            blocksize=512,
            latency='low',
        )
        self._stream.start()
        self._running = True

    def stop(self):
        if not self._running:
            return
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self._running = False

    @property
    def is_running(self):
        return self._running
