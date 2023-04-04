import os
import platform
import requests
import shutil
import subprocess


def check_ffmpeg_installed():
    try:
        # Run the ffmpeg command with the --version option and capture the output
        output = subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT)

        # Check if the output contains the expected version number
        if b"ffmpeg version" in output:
            return True
        else:
            return False
    except FileNotFoundError:
        # If the ffmpeg command is not found, the subprocess.check_output function
        # will raise a FileNotFoundError exception, which we catch and handle here
        return False


def install_ffmpeg_windows():
    # Download the ffmpeg binary archive from the official website
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Save the archive to a temporary file
    with open("ffmpeg.7z", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Extract the archive to the current directory
    shutil.unpack_archive("ffmpeg.7z", ".")

    # Add the ffmpeg executable directory to the system's PATH
    ffmpeg_path = os.path.abspath("ffmpeg-git-full/bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path


def install_ffmpeg_mac():
    # Install Homebrew package manager if not already installed
    if not shutil.which("brew"):
        subprocess.run("/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"", shell=True)

    # Install ffmpeg using Homebrew
    subprocess.run("brew install ffmpeg", shell=True)


def install_ffmpeg_linux():
    # Install ffmpeg using the system's package manager
    dist_name = platform.freedesktop_os_release()['ID_LIKE']
    if dist_name.lower() in ["debian", "ubuntu"]:
        subprocess.run("sudo apt-get install -y ffmpeg", shell=True)
    elif dist_name.lower() in ["centos", "redhat", "fedora"]:
        subprocess.run("sudo yum install -y ffmpeg", shell=True)
    else:
        raise Exception("Unsupported Linux distribution")
    

def install_ffmpeg():
    system = platform.system().lower()
    print(system)
    if system == "windows":
        install_ffmpeg_windows()
    elif system == "darwin":
        install_ffmpeg_mac()
    elif system == "linux":
        install_ffmpeg_linux()
    else:
        raise Exception("Unsupported operating system")