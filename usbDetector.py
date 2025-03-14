from tkinter import messagebox
import wmi
import time
import pythoncom

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
        for device in removed_usbs:
            root.after(0, lambda d=device: messagebox.showinfo("USB", f"Odłączono urządzenie: {d}"))
        prev_usbs = current_usbs
        time.sleep(2)