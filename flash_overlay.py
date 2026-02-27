import ctypes
import time

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget

from config import MOD_FREQ, TIMER_POLL_MS


# Improve Windows timer resolution from ~15.6ms to ~1ms
try:
    _winmm = ctypes.WinDLL('winmm')
    _winmm.timeBeginPeriod(1)
    _timer_resolution_set = True
except Exception:
    _timer_resolution_set = False


def restore_timer_resolution():
    if _timer_resolution_set:
        _winmm.timeEndPeriod(1)


class FlashOverlay(QWidget):
    """Transparent fullscreen overlay that flashes at 40Hz on a selected monitor."""

    def __init__(self, audio_engine=None):
        super().__init__()
        self._audio_engine = audio_engine
        self._flash_on = False
        self._intensity = 100  # 0-255 alpha for the dark overlay
        self._last_toggle = time.perf_counter()

        # Frameless, always-on-top, click-through, tool window (no taskbar entry)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Timer fires every 1ms; we do our own precise timing check inside
        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.timeout.connect(self._tick)

    def set_audio_engine(self, engine):
        self._audio_engine = engine

    def set_intensity(self, value):
        """Set flash intensity as 0-100 percentage."""
        self._intensity = int(value * 2.55)  # map 0-100 to 0-255

    def move_to_screen(self, screen):
        """Position the overlay to cover the given QScreen."""
        geo = screen.geometry()
        self.setGeometry(geo)

    def start_flashing(self):
        self._flash_on = False
        self._last_toggle = time.perf_counter()
        self.show()
        self._timer.start(TIMER_POLL_MS)

    def stop_flashing(self):
        self._timer.stop()
        self._flash_on = False
        self.hide()

    def _tick(self):
        """Check modulation phase from audio engine and update flash state."""
        if self._audio_engine and self._audio_engine.is_running:
            phase = self._audio_engine.get_modulation_phase()
            new_state = phase < 0.5
        else:
            # Fallback: free-running 40Hz toggle if no audio engine
            now = time.perf_counter()
            elapsed = now - self._last_toggle
            if elapsed >= 0.5 / MOD_FREQ:  # 12.5ms = half of 40Hz cycle
                self._last_toggle += 0.5 / MOD_FREQ
                new_state = not self._flash_on
            else:
                return

        if new_state != self._flash_on:
            self._flash_on = new_state
            self.update()

    def paintEvent(self, event):
        if self._flash_on:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(0, 0, 0, self._intensity))
            painter.end()
