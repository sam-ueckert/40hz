import sys

from PyQt6.QtWidgets import QApplication

from audio_engine import AudioEngine
from config import FLASH_INTENSITY, VOLUME_DEFAULT, VOLUME_MAX_AMPLITUDE
from control_panel import ControlPanel
from flash_overlay import FlashOverlay, restore_timer_resolution


def main():
    app = QApplication(sys.argv)
    screens = app.screens()

    audio = AudioEngine()
    overlay = FlashOverlay(audio_engine=audio)
    panel = ControlPanel()
    panel.populate_monitors(screens)

    selected_screen_index = 0

    def on_monitor_changed(index):
        nonlocal selected_screen_index
        selected_screen_index = index
        if index < len(screens):
            overlay.move_to_screen(screens[index])

    def on_start():
        if selected_screen_index < len(screens):
            overlay.move_to_screen(screens[selected_screen_index])
        audio.start()
        overlay.start_flashing()

    def on_stop():
        overlay.stop_flashing()
        audio.stop()

    def on_carrier_freq_changed(freq):
        audio.carrier_freq = float(freq)

    def on_intensity_changed(value):
        overlay.set_intensity(value)

    def on_volume_changed(value):
        audio.amplitude = value / 100.0 * VOLUME_MAX_AMPLITUDE

    # Wire signals
    panel.monitor_changed.connect(on_monitor_changed)
    panel.start_requested.connect(on_start)
    panel.stop_requested.connect(on_stop)
    panel.carrier_freq_changed.connect(on_carrier_freq_changed)
    panel.intensity_changed.connect(on_intensity_changed)
    panel.volume_changed.connect(on_volume_changed)

    # Set initial values from panel defaults
    on_intensity_changed(FLASH_INTENSITY)
    on_volume_changed(VOLUME_DEFAULT)
    if screens:
        on_monitor_changed(0)

    panel.show()

    exit_code = app.exec()
    on_stop()
    restore_timer_resolution()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
