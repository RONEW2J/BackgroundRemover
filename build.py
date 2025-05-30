import subprocess
import sys
import os


def install_requirements():
    """Install required packages"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def build_exe():
    """Build executable with PyInstaller"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=BackgroundRemover",
        "app.py"
    ]

    subprocess.check_call(cmd)


if __name__ == "__main__":
    print("Installing requirements...")
    install_requirements()

    print("Building executable...")
    build_exe()

    print("Build complete! Check the 'dist' folder.")
