import subprocess, sys, re

def enable_monitor(iface):
    subprocess.run(["sudo", "airmon-ng", "check", "kill"], check=True)
    result = subprocess.run(["sudo", "airmon-ng", "start", iface],
                            capture_output=True, text=True)
    # detect renamed interface e.g. "enabled on [phy11]wlan0mon"
    match = re.search(r"enabled (?:for|on) \[.*?\](\S+)", result.stdout)
    mon_iface = match.group(1) if match else iface + "mon"
    check = subprocess.run(["iwconfig", mon_iface], capture_output=True, text=True)
    if "Monitor" in check.stdout:
        print(f"[+] Monitor mode active on {mon_iface}")
        return mon_iface
    sys.exit(f"[-] Failed to enable monitor mode on {iface}")

def disable_monitor(mon_iface):
    subprocess.run(["sudo", "airmon-ng", "stop", mon_iface], check=True)
    print(f"[+] Monitor mode stopped on {mon_iface}")