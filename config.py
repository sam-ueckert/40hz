# 40Hz Gamma Entrainment — Configuration
# Edit these values to customize the application behavior.

# --- Audio ---
CARRIER_FREQ = 250.0        # Hz, carrier tone frequency
MOD_FREQ = 40.0             # Hz, modulation (entrainment) frequency
MOD_DEPTH = 1.0             # 0.0–1.0, amplitude modulation depth
AMPLITUDE = 0.3             # 0.0–1.0, master output volume
AUDIO_BLOCKSIZE = 512       # samples per audio callback
AUDIO_LATENCY = "low"       # "low", "high", or seconds (e.g. 0.01)

# --- Flash overlay ---
FLASH_INTENSITY = 40        # 0–100 %, default overlay darkness
TIMER_POLL_MS = 1           # ms, how often the overlay checks phase

# --- Control panel ---
WINDOW_TITLE = "40Hz Gamma Entrainment"
WINDOW_WIDTH = 380
CARRIER_FREQ_MIN = 100      # Hz
CARRIER_FREQ_MAX = 10000    # Hz
CARRIER_FREQ_STEP = 10      # Hz
VOLUME_DEFAULT = 30         # 0–100 %
VOLUME_MAX_AMPLITUDE = 0.3  # amplitude at 100% volume slider
MIN_REFRESH_RATE = 80       # Hz, warn if monitor is below this
