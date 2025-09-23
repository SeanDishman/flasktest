import os
import platform
import uuid
import hashlib
import subprocess
import requests

SERVER_URL = "https://flasktest-0b6f.onrender.com/validate"

def get_mac():
    try:
        return format(uuid.getnode(), "012x")
    except Exception:
        return ""

def get_cpu_info():
    p = platform.processor()
    if p:
        return p
    if platform.system().lower() == "linux":
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass
    try:
        out = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], stderr=subprocess.DEVNULL).decode().strip()
        if out:
            return out
    except Exception:
        pass
    return ""

def collect_fingerprint():
    items = {
        "mac": get_mac(),
        "platform": platform.platform(),
        "uname": " ".join(platform.uname()),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": get_cpu_info(),
        "cpu_count": str(os.cpu_count() or ""),
    }
    parts = []
    for k in sorted(items.keys()):
        parts.append(f"{k}={items[k]}")
    data = "|".join(parts)
    return data

def make_hwid_from_fingerprint(fingerprint):
    h = hashlib.sha512()
    h.update(fingerprint.encode("utf-8"))
    return h.hexdigest()

def send_hwid(hwid):
    payload = {"hwid": hwid}
    try:
        r = requests.post(SERVER_URL, json=payload, timeout=5)
        try:
            body = r.json()
        except Exception:
            body = r.text
        print("Status Code:", r.status_code)
        print("Response:", body)
    except Exception as e:
        print("Request failed:", str(e))

if __name__ == "__main__":
    fingerprint = collect_fingerprint()
    hwid = make_hwid_from_fingerprint(fingerprint)
    print("Generated HWID:", hwid)
    send_hwid(hwid)
