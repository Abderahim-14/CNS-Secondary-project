"""
config.py — S007 Global Configuration
======================================
Single source of truth for all runtime constants.
All modules import from here; nothing is hardcoded in module files.

Usage:
    import config
    iface = config.IFACE
"""

# ── Wireless Interface ────────────────────────────────────────────────────────
# Base interface name before monitor mode is enabled (e.g., wlan0, wlan1, wlan2).
# Update this after running: sudo airmon-ng
IFACE: str = "wlan1"

# Monitor-mode interface name created by airmon-ng (usually IFACE + "mon").
# This is set dynamically by monitor.py; kept here as a fallback reference.
MON_IFACE: str = "wlan1mon"

# ── Target AP (fill in after scanning) ───────────────────────────────────────
TARGET_BSSID: str = ""          # e.g., "AA:BB:CC:DD:EE:FF"
TARGET_CHANNEL: int = 6         # 802.11 channel the target AP operates on
TARGET_SSID: str = ""           # Human-readable name (reference only)

# ── Attack Defaults ───────────────────────────────────────────────────────────
DEFAULT_RATE: int = 500         # Frames per second (beacon / deauth modes)
DEFAULT_DURATION: int = 60      # Attack duration in seconds
DEFAULT_CLIENT: str = "ff:ff:ff:ff:ff:ff"   # Broadcast — targets all clients
DEFAULT_BEACON_SSID: str = ""   # Empty → generate random SSIDs each frame

# ── Scanner Defaults ──────────────────────────────────────────────────────────
SCAN_TIMEOUT: int = 20          # Seconds before scan() returns results
HOP_INTERVAL: float = 0.3       # Seconds spent on each channel during hopping

# 2.4 GHz channels (1–13 covers most regulatory domains)
CHANNELS_2GHZ: list[int] = list(range(1, 14))

# Common 5 GHz channels (UNII-1 / UNII-2) — extend if your card supports more
CHANNELS_5GHZ: list[int] = [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112]

# ── Flood Defaults ────────────────────────────────────────────────────────────
FLOOD_MIN_PAYLOAD: int = 100    # Minimum random payload size in bytes
FLOOD_MAX_PAYLOAD: int = 1400   # Maximum random payload size in bytes

# ── Paths ─────────────────────────────────────────────────────────────────────
RESULTS_DIR: str = "results/"
CAPTURES_DIR: str = "captures/"
LOG_DIR: str = "logs/"

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL: str = "INFO"         # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE: bool = False       # Set True to also write logs to LOG_DIR