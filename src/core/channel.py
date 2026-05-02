import subprocess, time

def lock_channel(iface, channel):
    """Fix adapter to a specific 802.11 channel."""
    subprocess.run(["sudo", "iwconfig", iface, "channel", str(channel)], check=True)
    print(f"[+] Locked {iface} to channel {channel}")

def hop_channels(iface, channels=None, interval=0.3, stop_event=None):
    """Cycle adapter through channels during scanning."""
    if channels is None:
        channels = list(range(1, 14))
    import threading
    if stop_event is None:
        stop_event = threading.Event()
    while not stop_event.is_set():
        for ch in channels:
            if stop_event.is_set():
                break
            subprocess.run(["sudo", "iwconfig", iface, "channel", str(ch)],
                           capture_output=True)
            time.sleep(interval)
