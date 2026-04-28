import subprocess, sys

def enable_monitor(iface):
    subprocess.run(["sudo", "airmon-ng", "check", "kill"], check=True)
    subprocess.run(["sudo", "airmon-ng", "start", iface], check=True)
    mon_iface = iface + "mon"
    result = subprocess.run(["iwconfig", mon_iface], capture_output=True, text=True)
    if "Monitor" in result.stdout:
        print(f"[+] Monitor mode active on {mon_iface}")
        return mon_iface
    sys.exit(f"[-] Failed to enable monitor mode on {iface}")

def disable_monitor(mon_iface):
    subprocess.run(["sudo", "airmon-ng", "stop", mon_iface], check=True)
    print(f"[+] Monitor mode stopped on {mon_iface}")
