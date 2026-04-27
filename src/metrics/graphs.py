# src/metrics/graphs.py
import pandas as pd
import matplotlib.pyplot as plt
import os

OUTDIR = "results/graphs"
os.makedirs(OUTDIR, exist_ok=True)


def throughput_timeline(csv_paths: dict, title="Throughput Over Time"):
    """csv_paths: {'Baseline WPA2': 'path.csv', 'Beacon Flood WPA2': 'path.csv', ...}"""
    fig, ax = plt.subplots(figsize=(12, 5))
    for label, path in csv_paths.items():
        df = pd.read_csv(path)
        ax.plot(df["start_s"], df["throughput_mbps"], label=label, linewidth=1.5)
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Throughput (Mbps)")
    ax.set_title(title); ax.legend(); ax.grid(True, alpha=0.3)
    out = f"{OUTDIR}/throughput_timeline.png"
    plt.savefig(out, dpi=150, bbox_inches="tight"); plt.close()
    print(f"[+] Saved {out}")


def wpa2_vs_wpa3_bar(results: dict, title="WPA2 vs. WPA3 — Avg Throughput Under Attack"):
    """results: {'Beacon WPA2': 12.3, 'Beacon WPA3': 34.1, ...}"""
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = list(results.keys()); values = list(results.values())
    colors = ["#e05252" if "WPA2" in l else "#5280e0" for l in labels]
    bars = ax.bar(labels, values, color=colors, width=0.5)
    ax.bar_label(bars, fmt="%.1f Mbps", padding=4, fontsize=9)
    ax.set_ylabel("Average Throughput (Mbps)"); ax.set_title(title)
    plt.xticks(rotation=15, ha="right"); ax.grid(axis="y", alpha=0.3)
    out = f"{OUTDIR}/wpa2_vs_wpa3_bar.png"
    plt.savefig(out, dpi=150, bbox_inches="tight"); plt.close()
    print(f"[+] Saved {out}")


def frame_rate_timeline(csv_path, frame_col, title, filename):
    """Plot per-second frame rate from parser CSV."""
    df = pd.read_csv(csv_path)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.fill_between(range(len(df)), df[frame_col], alpha=0.4)
    ax.plot(df[frame_col], linewidth=1.2)
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Frames/sec")
    ax.set_title(title); ax.grid(True, alpha=0.3)
    out = f"{OUTDIR}/{filename}"
    plt.savefig(out, dpi=150, bbox_inches="tight"); plt.close()
    print(f"[+] Saved {out}")


def packet_loss_bar(results: dict, title="Packet Loss % by Attack Mode and Security"):
    """results: {'Beacon WPA2': 72.1, 'Beacon WPA3': 61.4, ...}"""
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = list(results.keys()); values = list(results.values())
    colors = ["#e05252" if "WPA2" in l else "#5280e0" for l in labels]
    bars = ax.bar(labels, values, color=colors, width=0.5)
    ax.bar_label(bars, fmt="%.1f%%", padding=4, fontsize=9)
    ax.set_ylabel("Packet Loss (%)"); ax.set_title(title); ax.set_ylim(0, 110)
    plt.xticks(rotation=15, ha="right"); ax.grid(axis="y", alpha=0.3)
    out = f"{OUTDIR}/packet_loss_bar.png"
    plt.savefig(out, dpi=150, bbox_inches="tight"); plt.close()
    print(f"[+] Saved {out}")


def wids_latency_boxplot(latencies: dict, title="WIDS Alert Latency by Attack Mode"):
    """latencies: {'Beacon': [1.2, 0.9, 1.5, ...], 'Deauth': [...], 'Flood': [...]}"""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(latencies.values(), labels=latencies.keys(), patch_artist=True)
    ax.set_ylabel("Alert Latency (s)"); ax.set_title(title); ax.grid(axis="y", alpha=0.3)
    out = f"{OUTDIR}/wids_latency_boxplot.png"
    plt.savefig(out, dpi=150, bbox_inches="tight"); plt.close()
    print(f"[+] Saved {out}")