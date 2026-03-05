import hashlib
import os
import json
import time

# Configuration
MONITOR_DIR = "./my_secure_files"  # Folder to watch
BASELINE_FILE = "baseline.json"     # Trusted fingerprint storage

def calculate_sha256(filepath):
    """Calculates SHA-256 hash in 4096-byte chunks for memory efficiency."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read file in blocks to handle large files without crashing
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def create_baseline(directory):
    """Scans directory and saves current file fingerprints to JSON."""
    baseline = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_hash = calculate_sha256(full_path)
            if file_hash:
                baseline[full_path] = file_hash
    
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)
    print(f"[+] Baseline created with {len(baseline)} files.")

def monitor_integrity(directory):
    """Compares current file states against the saved baseline."""
    if not os.path.exists(BASELINE_FILE):
        print("[-] No baseline found. Run --baseline first.")
        return

    with open(BASELINE_FILE, "r") as f:
        baseline = json.load(f)

    print("[*] Monitoring started... (Press Ctrl+C to stop)")
    while True:
        try:
            current_files = []
            for root, _, files in os.walk(directory):
                for file in files:
                    full_path = os.path.join(root, file)
                    current_files.append(full_path)
                    current_hash = calculate_sha256(full_path)

                    # Check for modifications or new files
                    if full_path not in baseline:
                        print(f"[ALERT] NEW FILE DETECTED: {full_path}")
                        baseline[full_path] = current_hash # Auto-update baseline
                    elif current_hash != baseline[full_path]:
                        print(f"[ALERT] FILE MODIFIED: {full_path}")
                        baseline[full_path] = current_hash # Auto-update baseline

            # Check for deletions
            for path in list(baseline.keys()):
                if path not in current_files:
                    print(f"[ALERT] FILE DELETED: {path}")
                    del baseline[path]

            time.sleep(2) # Scan interval
        except KeyboardInterrupt:
            print("\n[*] Monitoring stopped.")
            break

if __name__ == "__main__":
    # Quick CLI logic
    choice = input("Enter 'b' to Create Baseline or 'm' to Monitor: ").lower()
    if choice == 'b':
        create_baseline(MONITOR_DIR)
    elif choice == 'm':
        monitor_integrity(MONITOR_DIR)
