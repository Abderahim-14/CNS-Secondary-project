# src/metrics/capture.py
import subprocess, os, signal, time

class CaptureSession:
    def __init__(self, iface, output_path):
        self.iface = iface
        self.output_path = output_path
        self.proc = None

    def start(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        cmd = ["sudo", "tshark", "-i", self.iface, "-w", self.output_path]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
        print(f"[+] Capture started → {self.output_path} (PID {self.proc.pid})")

    def stop(self):
        if self.proc:
            self.proc.send_signal(signal.SIGTERM)
            self.proc.wait()
            print(f"[+] Capture stopped — saved to {self.output_path}")

    def __enter__(self):
        self.start(); return self

    def __exit__(self, *args):
        self.stop()