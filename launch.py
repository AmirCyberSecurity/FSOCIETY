import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    requirements = os.path.join(BASE_DIR, "requirements.txt")
    application = os.path.join(BASE_DIR, "fsociety.py")

    print("[*] Installing dependencies...")

    result = subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", requirements
    ])

    if result.returncode != 0:
        print("[!] Failed to install dependencies.")
        sys.exit(1)

    os.system("cls" if os.name == "nt" else "clear")

    print("[*] Starting fsociety...\n")

    subprocess.run([sys.executable, application])


if __name__ == "__main__":
    main()
