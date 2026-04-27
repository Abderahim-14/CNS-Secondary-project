# src/metrics/throughput.py
import subprocess, json, csv, os

def run_iperf3(server_ip, duration=60, output_json_path=None, udp=False, bandwidth="100M"):
    """Run iperf3 client and save JSON output."""
    cmd = ["iperf3", "-c", server_ip, "-t", str(duration), "-J"]
    if udp:
        cmd += ["-u", "-b", bandwidth]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    if output_json_path:
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, "w") as f:
            json.dump(data, f, indent=2)
    return data

def parse_iperf3_json(json_path, output_csv_path):
    """Extract per-interval Mbps from iperf3 JSON and write to CSV."""
    with open(json_path) as f:
        data = json.load(f)
    intervals = data.get("intervals", [])
    rows = []
    for interval in intervals:
        start = interval["sum"]["start"]
        end   = interval["sum"]["end"]
        mbps  = interval["sum"]["bits_per_second"] / 1e6
        lost  = interval["sum"].get("lost_percent", 0)
        rows.append({
            "start_s":         round(start, 1),
            "end_s":           round(end,   1),
            "throughput_mbps": round(mbps,  3),
            "lost_pct":        round(lost,  2),
        })
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"[+] Throughput CSV written → {output_csv_path}")
    return rows