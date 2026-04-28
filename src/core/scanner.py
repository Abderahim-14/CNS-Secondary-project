from scapy.all import *
import threading

discovered = {}

def handle_beacon(pkt):
    if not pkt.haslayer(Dot11Beacon):
        return
    bssid = pkt[Dot11].addr3
    try:
        ssid = pkt[Dot11Elt].info.decode(errors='ignore') or ''
    except Exception:
        ssid = ''
    # Extract channel
    ch_elt = pkt.getlayer(Dot11Elt, ID=3)
    channel = int(ord(ch_elt.info)) if ch_elt else 0
    # Extract capabilities
    cap = pkt[Dot11Beacon].cap
    if bssid not in discovered:
        discovered[bssid] = {'ssid': ssid, 'channel': channel, 'bssid': bssid}
        print(f"  [{len(discovered):>3}] SSID: {ssid:30s} BSSID: {bssid}  CH: {channel:>2}")

def scan(iface, timeout=20):
    print(f"[*] Scanning on {iface} for {timeout}s...\n")
    sniff(iface=iface, prn=handle_beacon, store=False, timeout=timeout)
    return list(discovered.values())