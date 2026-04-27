# src/metrics/parser.py
import pyshark, csv, os
from collections import defaultdict

FRAME_TYPES = {
    "beacon":   "wlan.fc.type_subtype == 8",
    "deauth":   "wlan.fc.type_subtype == 12",
    "disassoc": "wlan.fc.type_subtype == 10",
    "probe_req":"wlan.fc.type_subtype == 4",
}

def count_frames_per_second(pcap_path, output_csv_path):
    """Parse a .pcapng file and output per-second frame type counts."""
    cap = pyshark.FileCapture(pcap_path, keep_packets=False)
    per_second = defaultdict(lambda: defaultdict(int))
    for pkt in cap:
        try:
            ts      = int(float(pkt.sniff_timestamp))
            subtype = int(pkt.wlan.fc_type_subtype, 16)
            per_second[ts]["total"] += 1
            if subtype == 8:  per_second[ts]["beacon"]  += 1
            if subtype == 12: per_second[ts]["deauth"]  += 1
            if subtype == 10: per_second[ts]["disassoc"]+= 1
        except AttributeError:
            continue
    cap.close()
    rows = [{"second": ts, **counts} for ts, counts in sorted(per_second.items())]
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    if rows:
        with open(output_csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    print(f"[+] Frame count CSV written → {output_csv_path}")
    return rows