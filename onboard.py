import platform
import subprocess

# Example of how to safely call PowerShell only if running on Windows
powershell_cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "create_user.ps1"]

if platform.system() == "Windows":
    # Run the actual PowerShell script on Windows
    subprocess.run(powershell_cmd, check=True)
else:
    # Simulate execution on Linux/GitHub Codespaces (Dry-Run mode)
    print(
        f"[Linux/Codespaces Notice] Simulated PowerShell execution: {' '.join(powershell_cmd)}"
    )