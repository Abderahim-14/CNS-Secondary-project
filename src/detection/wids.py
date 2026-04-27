# src/detection/wids.py
import time, csv, os, argparse
from scapy.all import *
from detection.signatures import check_signatures


class WIDS:
    def __init__(self, iface, log_path="results/wids_alerts.csv"):
        self.iface       = iface
        self.log_path    = log_path
        self.window      = {"beacon": 0, "deauth": 0, "disassoc": 0,
                            "total": 0, "unique_bssids": set()}
        self.window_start = time.time()
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self._init_log()

    def _init_log(self):
        with open(self.log_path, "w", newline="") as f:
            csv.writer(f).writerow(["timestamp", "sig_id", "description",
                                    "value", "threshold"])

    def _log_alert(self, sig_id, description, value, threshold):
        ts = time.strftime("%H:%M:%S")
        print(f"[ALERT {sig_id}] {description} | measured: {value:.1f} | "
              f"threshold: {threshold}")
        with open(self.log_path, "a", newline="") as f:
            csv.writer(f).writerow([ts, sig_id, description,
                                    round(value, 2), threshold])

    def _handle(self, pkt):
        self.window["total"] += 1
        if pkt.haslayer(Dot11Beacon):
            self.window["beacon"] += 1
            try:
                self.window["unique_bssids"].add(pkt[Dot11].addr3)
            except Exception:
                pass
        if pkt.haslayer(Dot11Deauth):
            self.window["deauth"] += 1
        if pkt.haslayer(Dot11Disas):
            self.window["disassoc"] += 1

        elapsed = time.time() - self.window_start
        if elapsed >= 1.0:
            alerts = check_signatures(self.window, elapsed)
            for sig_id, desc, val, thresh in alerts:
                self._log_alert(sig_id, desc, val, thresh)
            # Reset window
            self.window = {"beacon": 0, "deauth": 0, "disassoc": 0,
                           "total": 0, "unique_bssids": set()}
            self.window_start = time.time()

    def run(self):
        print(f"[*] WIDS active on {self.iface} — monitoring for anomalies...")
        print(f"[*] Alerts will be logged to {self.log_path}")
        sniff(iface=self.iface, prn=self._handle, store=False)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="S007 WIDS — Real-time anomaly detector")
    p.add_argument("--iface",   required=True, help="Monitor-mode interface (e.g. wlan2mon)")
    p.add_argument("--log",     default="results/wids_alerts.csv", help="Alert CSV output path")
    args = p.parse_args()
    wids = WIDS(iface=args.iface, log_path=args.log)
    wids.run()