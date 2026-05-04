#!/bin/bash
# experiments/run_attack.sh
# Capture metrics during an active attack session.
# Member 1 launches the attack separately on the attacker machine.
# Usage: sudo bash run_attack.sh beacon wpa2

MODE="${1:-beacon}"        # beacon | deauth | flood
SECURITY="${2:-wpa2}"      # wpa2   | wpa3
IFACE_MON="wlp1s0mon"       # wlan2mon
SERVER_IP="192.168.10.10"
DURATION=60
OUTDIR="results/raw"
mkdir -p "$OUTDIR" captures

LABEL="${MODE}_${SECURITY}"

echo "[*] Starting capture for run: $LABEL"
sudo tshark -i "$IFACE_MON" -w "captures/${LABEL}.pcapng" &
TSHARK_PID=$!
sleep 1

echo "[*] Starting iperf3 TCP during attack ($DURATION s) ..."
iperf3 -c "$SERVER_IP" -t "$DURATION" -J > "$OUTDIR/${LABEL}_tcp.json" &
IPERF_PID=$!

echo "[*] Launching attack: ${MODE} on ${SECURITY} AP..."
# NOTE: Attack is launched separately by Member 1 on the attacker machine.
# Coordinate timing — Member 1 should start injection now.

wait "$IPERF_PID"
kill "$TSHARK_PID"
wait "$TSHARK_PID" 2>/dev/null
echo "[+] Run complete: ${LABEL}"
echo "[+] Capture: captures/${LABEL}.pcapng"
echo "[+] iperf3:  $OUTDIR/${LABEL}_tcp.json"