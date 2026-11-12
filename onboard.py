import subprocess
import sys
import secrets
import string
import logging
import pandas as pd

logging.basicConfig(
    filename="onboarding_audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def generate_temp_password(length=14):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in pwd) and any(c.isupper() for c in pwd)
                and any(c.isdigit() for c in pwd) and any(c in "!@#$%^&*" for c in pwd)):
            return pwd

def provision_users(csv_path, dry_run=False):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        password = str(row['TemporaryPassword']) if pd.notna(row.get('TemporaryPassword')) else generate_temp_password()
        
        cmd = [
            "powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "create_user.ps1",
            "-Username", str(row['Username']),
            "-FirstName", str(row['FirstName']),
            "-LastName", str(row['LastName']),
            "-Department", str(row['Department']),
            "-Password", password
        ]
        if dry_run:
            cmd.append("-DryRun")

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            msg = f"Provisioned {row['Username']} ({row['Department']}) | DryRun={dry_run}"
            print(f"OK: {result.stdout.strip()}")
            logging.info(msg)
        else:
            err = f"Failed {row['Username']}: {result.stderr.strip()}"
            print(f"ERROR: {err}")
            logging.error(err)

if __name__ == "__main__":
    is_dry_run = "--dry-run" in sys.argv
    provision_users("new_hires.csv", dry_run=is_dry_run)
