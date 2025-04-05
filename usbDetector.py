from tkinter import messagebox
import wmi
import time
import pythoncom

from logHistory import add_log
from signFile import load_key


def monitor_usb(root,log_text):
    pythoncom.CoInitialize()
    c = wmi.WMI()
    prev_usbs = {d.DeviceID for d in c.Win32_DiskDrive() if 'USB' in d.Caption}
    while True:
        current_usbs = {d.DeviceID for d in c.Win32_DiskDrive() if 'USB' in d.Caption}
        added_usbs = current_usbs - prev_usbs
        removed_usbs = prev_usbs - current_usbs
        for device in added_usbs:
            add_log(log_text, f"Podłączono urządzenie: {device}")

            for drive in c.Win32_DiskDrive():
                if drive.DeviceID == device:
                    partitions = drive.associators(wmi_result_class="Win32_DiskPartition")
                    for partition in partitions:
                        logical_disks = partition.associators(wmi_result_class="Win32_LogicalDisk")
                        for logical_disk in logical_disks:
                            if logical_disk.DriveType == 2:
                                usb_path = logical_disk.DeviceID
                                if usb_path:
                                    load_key(usb_path,log_text)
                                    break
        for device in removed_usbs:
            add_log(log_text, f"Odłączono urządzenie: {device}")
        prev_usbs = current_usbs
        time.sleep(2)