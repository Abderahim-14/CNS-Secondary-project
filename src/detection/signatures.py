# src/detection/signatures.py

SIGNATURES = [
    ("SIG-001", "Beacon flood",          "beacon",        200),
    ("SIG-002", "Deauth burst",          "deauth",         50),
    ("SIG-003", "High mgmt-frame ratio", "mgmt_ratio",   0.80),
    ("SIG-004", "Spoofed beacon farm",   "unique_bssids",  50),
    ("SIG-005", "Disassoc flood",        "disassoc",       30),
]

def check_signatures(window, elapsed):
    """
    Evaluate all signatures against a 1-second window snapshot.
    Returns list of (sig_id, description, measured_value, threshold) tuples.
    """
    beacon_rate   = window["beacon"]   / elapsed
    deauth_rate   = window["deauth"]   / elapsed
    disassoc_rate = window["disassoc"] / elapsed
    mgmt_ratio    = (window["beacon"] + window["deauth"] + window["disassoc"]) \
                    / max(window["total"], 1)
    bssid_rate    = len(window["unique_bssids"]) / elapsed

    checks = [
        ("SIG-001", "Beacon flood detected",         beacon_rate,   200),
        ("SIG-002", "Deauth burst detected",          deauth_rate,    50),
        ("SIG-003", "High management-frame ratio",   mgmt_ratio,   0.80),
        ("SIG-004", "Spoofed beacon farm detected",  bssid_rate,     50),
        ("SIG-005", "Disassociation flood detected", disassoc_rate,  30),
    ]

    alerts = []
    for sig_id, desc, value, threshold in checks:
        if value > threshold:
            alerts.append((sig_id, desc, value, threshold))
    return alerts