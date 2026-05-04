from throughput import parse_iperf3_json
from parser import count_frames_per_second
from graphs import *


# ── Parse iperf3 JSON → CSV ──────────────────────────────────────────────────
parse_iperf3_json('results/raw/baseline_tcp.json',    'results/processed/baseline_tcp.csv')
parse_iperf3_json('results/raw/beacon_wpa2_tcp.json', 'results/processed/beacon_wpa2.csv')
parse_iperf3_json('results/raw/deauth_wpa2_tcp.json', 'results/processed/deauth_wpa2.csv')
parse_iperf3_json('results/raw/flood_wpa2_tcp.json',  'results/processed/flood_wpa2.csv')
parse_iperf3_json('results/raw/beacon_wpa3_tcp.json', 'results/processed/beacon_wpa3.csv')
parse_iperf3_json('results/raw/deauth_wpa3_tcp.json', 'results/processed/deauth_wpa3.csv')
parse_iperf3_json('results/raw/flood_wpa3_tcp.json',  'results/processed/flood_wpa3.csv')

# ── Parse pcapng → frame count CSV ──────────────────────────────────────────
count_frames_per_second('captures/baseline.pcapng',    'results/processed/baseline_frames.csv')
count_frames_per_second('captures/beacon_wpa2.pcapng', 'results/processed/beacon_wpa2_frames.csv')
count_frames_per_second('captures/deauth_wpa2.pcapng', 'results/processed/deauth_wpa2_frames.csv')
count_frames_per_second('captures/flood_wpa2.pcapng',  'results/processed/flood_wpa2_frames.csv')
count_frames_per_second('captures/beacon_wpa3.pcapng', 'results/processed/beacon_wpa3_frames.csv')
count_frames_per_second('captures/deauth_wpa3.pcapng', 'results/processed/deauth_wpa3_frames.csv')
count_frames_per_second('captures/flood_wpa3.pcapng',  'results/processed/flood_wpa3_frames.csv')

# ── Generate graphs ──────────────────────────────────────────────────────────
throughput_timeline({
    'Baseline':    'results/processed/baseline_tcp.csv',
    'Beacon WPA2': 'results/processed/beacon_wpa2.csv',
    'Deauth WPA2': 'results/processed/deauth_wpa2.csv',
    'Flood WPA2':  'results/processed/flood_wpa2.csv',
    'Beacon WPA3': 'results/processed/beacon_wpa3.csv',
    'Deauth WPA3': 'results/processed/deauth_wpa3.csv',
    'Flood WPA3':  'results/processed/flood_wpa3.csv',
})

frame_rate_timeline('results/processed/beacon_wpa2_frames.csv', 'beacon', 'Beacon Rate WPA2', 'beacon_rate_wpa2.png')
frame_rate_timeline('results/processed/deauth_wpa2_frames.csv', 'deauth', 'Deauth Rate WPA2', 'deauth_rate_wpa2.png')

wpa2_vs_wpa3_bar({
    'Beacon WPA2': 'results/processed/beacon_wpa2.csv',
    'Beacon WPA3': 'results/processed/beacon_wpa3.csv',
    'Deauth WPA2': 'results/processed/deauth_wpa2.csv',
    'Deauth WPA3': 'results/processed/deauth_wpa3.csv',
    'Flood WPA2':  'results/processed/flood_wpa2.csv',
    'Flood WPA3':  'results/processed/flood_wpa3.csv',
})

packet_loss_bar({
    'Beacon WPA2': 'results/processed/beacon_wpa2.csv',
    'Beacon WPA3': 'results/processed/beacon_wpa3.csv',
    'Deauth WPA2': 'results/processed/deauth_wpa2.csv',
    'Deauth WPA3': 'results/processed/deauth_wpa3.csv',
    'Flood WPA2':  'results/processed/flood_wpa2.csv',
    'Flood WPA3':  'results/processed/flood_wpa3.csv',
})

wids_latency_boxplot({
    'Beacon': 'results/wids_alerts.csv',
    'Deauth': 'results/wids_alerts.csv',
    'Flood':  'results/wids_alerts.csv',
})

print("\n[+] All done — check results/graphs/")