# loader.py
import os
from datetime import datetime

def load_hostnames(path):
    """Load hostnames from file, ignore blank lines or comments, support comma-separated"""
    if not os.path.exists(path):
        return []
    hosts = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            hosts.extend([h.strip() for h in line.split(",") if h.strip()])
    return hosts

def load_dates(path):
    """Load dates from file, ignoring comments"""
    if not os.path.exists(path):
        return []
    dates = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                dt = datetime.strptime(line, "%Y-%m-%d")
                dates.append((False, dt))
            except ValueError:
                try:
                    dt = datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
                    dates.append((True, dt))
                except ValueError:
                    print(f"Warning: ignoring invalid date line: {line}")
    return dates

def load_timelapse(path):
    """Load min,max timelapse in seconds"""
    if not os.path.exists(path):
        return 0.0, 0.0
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) == 1:
                val = float(parts[0])
                return val, val
            elif len(parts) >= 2:
                return float(parts[0]), float(parts[1])
    return 0.0, 0.0
