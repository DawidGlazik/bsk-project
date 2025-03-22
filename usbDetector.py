from tkinter import messagebox
import wmi
import time
import pythoncom

from signFile import load_key


def monitor_usb(root):
    pythoncom.CoInitialize()
    c = wmi.WMI()
    prev_usbs = {d.DeviceID for d in c.Win32_DiskDrive() if 'USB' in d.Caption}
    while True:
        current_usbs = {d.DeviceID for d in c.Win32_DiskDrive() if 'USB' in d.Caption}
        added_usbs = current_usbs - prev_usbs
        removed_usbs = prev_usbs - current_usbs
        for device in added_usbs:
            root.after(0, lambda d=device: messagebox.showinfo("USB", f"Podłączono urządzenie: {d}"))

            for drive in c.Win32_DiskDrive():
                if drive.DeviceID == device:
                    partitions = drive.associators(wmi_result_class="Win32_DiskPartition")
                    for partition in partitions:
                        logical_disks = partition.associators(wmi_result_class="Win32_LogicalDisk")
                        for logical_disk in logical_disks:
                            if logical_disk.DriveType == 2:
                                usb_path = logical_disk.DeviceID
                                if usb_path:
                                    load_key(usb_path)
                                    break
        for device in removed_usbs:
            root.after(0, lambda d=device: messagebox.showinfo("USB", f"Odłączono urządzenie: {d}"))
        prev_usbs = current_usbs
        time.sleep(2)