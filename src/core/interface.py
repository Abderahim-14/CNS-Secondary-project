def detect_adapters():
    """Return list of wireless interfaces and their monitor-mode capability."""
    result = subprocess.run(["sudo", "airmon-ng"], capture_output=True, text=True)
    adapters = re.findall(r'(wlan\w+)\s+\w+\s+(\w+)', result.stdout)
    return adapters

def check_injection_capable(iface):
    """Verify adapter supports packet injection."""
    result = subprocess.run(["sudo", "aireplay-ng", "--test", iface],
                            capture_output=True, text=True)
    return "Injection is working" in result.stdout

if __name__ == "__main__":
    for iface, driver in detect_adapters():
        capable = check_injection_capable(iface)
        print(f"[{'OK' if capable else 'FAIL'}] {iface} ({driver}) — injection: {capable}")