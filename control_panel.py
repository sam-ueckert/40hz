from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class ControlPanel(QWidget):
    """Control GUI for the 40Hz gamma entrainment app."""

    start_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    monitor_changed = pyqtSignal(int)
    carrier_freq_changed = pyqtSignal(int)
    intensity_changed = pyqtSignal(int)
    volume_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._running = False
        self._screens = []
        self.setWindowTitle("40Hz Gamma Entrainment")
        self.setFixedWidth(380)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Monitor selector
        layout.addWidget(QLabel("Monitor:"))
        self._monitor_combo = QComboBox()
        self._monitor_combo.currentIndexChanged.connect(self._on_monitor_changed)
        layout.addWidget(self._monitor_combo)

        # Refresh rate warning
        self._refresh_warning = QLabel()
        self._refresh_warning.setStyleSheet("color: #b8860b; font-weight: bold;")
        self._refresh_warning.setWordWrap(True)
        self._refresh_warning.hide()
        layout.addWidget(self._refresh_warning)

        # Carrier frequency
        freq_row = QHBoxLayout()
        freq_row.addWidget(QLabel("Carrier Freq (Hz):"))
        self._freq_spin = QSpinBox()
        self._freq_spin.setRange(100, 10000)
        self._freq_spin.setValue(250)
        self._freq_spin.setSingleStep(10)
        self._freq_spin.valueChanged.connect(self.carrier_freq_changed.emit)
        freq_row.addWidget(self._freq_spin)
        layout.addLayout(freq_row)

        # Flash intensity
        intensity_row = QHBoxLayout()
        intensity_row.addWidget(QLabel("Flash Intensity:"))
        self._intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self._intensity_slider.setRange(0, 100)
        self._intensity_slider.setValue(40)
        self._intensity_slider.valueChanged.connect(self.intensity_changed.emit)
        intensity_row.addWidget(self._intensity_slider)
        self._intensity_label = QLabel("40%")
        self._intensity_slider.valueChanged.connect(
            lambda v: self._intensity_label.setText(f"{v}%")
        )
        intensity_row.addWidget(self._intensity_label)
        layout.addLayout(intensity_row)

        # Volume
        volume_row = QHBoxLayout()
        volume_row.addWidget(QLabel("Volume:"))
        self._volume_slider = QSlider(Qt.Orientation.Horizontal)
        self._volume_slider.setRange(0, 100)
        self._volume_slider.setValue(30)
        self._volume_slider.valueChanged.connect(self.volume_changed.emit)
        volume_row.addWidget(self._volume_slider)
        self._volume_label = QLabel("30%")
        self._volume_slider.valueChanged.connect(
            lambda v: self._volume_label.setText(f"{v}%")
        )
        volume_row.addWidget(self._volume_label)
        layout.addLayout(volume_row)

        # Start/Stop button
        self._toggle_btn = QPushButton("Start")
        self._toggle_btn.setStyleSheet(
            "QPushButton { padding: 10px; font-size: 16px; font-weight: bold; }"
        )
        self._toggle_btn.clicked.connect(self._on_toggle)
        layout.addWidget(self._toggle_btn)

        # Status
        self._status_label = QLabel("Stopped")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status_label)

    def populate_monitors(self, screens):
        """Populate the monitor dropdown from a list of QScreen objects."""
        self._screens = screens
        self._monitor_combo.clear()
        for i, screen in enumerate(screens):
            geo = screen.geometry()
            rate = screen.refreshRate()
            name = screen.name() or f"Monitor {i + 1}"
            label = f"{name}  ({geo.width()}x{geo.height()} @ {rate:.0f}Hz)"
            self._monitor_combo.addItem(label)
        if screens:
            self._on_monitor_changed(0)

    def _on_monitor_changed(self, index):
        if 0 <= index < len(self._screens):
            rate = self._screens[index].refreshRate()
            if rate < 80:
                self._refresh_warning.setText(
                    f"Warning: This monitor runs at {rate:.0f}Hz. "
                    f"40Hz flashing requires 80Hz+ for frame-accurate display. "
                    f"The flash will still work but timing will be uneven."
                )
                self._refresh_warning.show()
            else:
                self._refresh_warning.hide()
            self.monitor_changed.emit(index)

    def _on_toggle(self):
        if self._running:
            self.stop_requested.emit()
            self._running = False
            self._toggle_btn.setText("Start")
            self._status_label.setText("Stopped")
            self._status_label.setStyleSheet("")
        else:
            self.start_requested.emit()
            self._running = True
            self._toggle_btn.setText("Stop")
            self._status_label.setText("Running — 40Hz entrainment active")
            self._status_label.setStyleSheet("color: green; font-weight: bold;")
