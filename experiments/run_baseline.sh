#!/bin/bash
# experiments/run_baseline.sh
# Run baseline iperf3 + tshark capture before any attack is launched.

IFACE_MON="wlan2mon"          # capture interface in monitor mode
SERVER_IP="192.168.10.10"     # iperf3 server (Client 1)
OUTDIR="results/raw"
mkdir -p "$OUTDIR" captures

echo "[*] Starting baseline capture on $IFACE_MON ..."
sudo tshark -i "$IFACE_MON" -w captures/baseline.pcapng &
TSHARK_PID=$!
sleep 1   # let tshark spin up

echo "[*] Running iperf3 baseline TCP (60 s) ..."
iperf3 -c "$SERVER_IP" -t 60 -J > "$OUTDIR/baseline_tcp.json"

echo "[*] Running iperf3 baseline UDP (60 s) ..."
iperf3 -c "$SERVER_IP" -u -b 100M -t 60 -J > "$OUTDIR/baseline_udp.json"

kill "$TSHARK_PID"
wait "$TSHARK_PID" 2>/dev/null
echo "[+] Baseline complete. Files saved to $OUTDIR and captures/."