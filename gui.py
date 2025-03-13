import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import wmi
import time

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def sign_document():
    file_path = entry_file.get()
    pin = entry_pin.get()
    if not file_path or not pin:
        messagebox.showerror("Błąd", "Wybierz plik PDF i wpisz PIN.")

def verify_signature():
    file_path = entry_file.get()
    if not file_path:
        messagebox.showerror("Błąd", "Wybierz plik PDF do weryfikacji.")

def show_signing_view():
    verification_screen.pack_forget()
    signing_screen.pack(pady=10)

def show_verification_view():
    signing_screen.pack_forget()
    verification_screen.pack(pady=10)

def signing_view(root):
    signing_screen = tk.Frame(root)
    tk.Label(signing_screen, text="Plik PDF:").pack(pady=5)
    entry_file = tk.Entry(signing_screen, width=40)
    entry_file.pack()
    tk.Button(signing_screen, text="Wybierz plik", command=select_file).pack(pady=5)
    tk.Label(signing_screen, text="PIN:").pack(pady=5)
    entry_pin = tk.Entry(signing_screen, show="*", width=20)
    entry_pin.pack()
    tk.Button(signing_screen, text="Podpisz dokument", command=sign_document).pack(pady=10)
    
    return signing_screen, entry_file, entry_pin

def verification_view(root):
    verification_screen = tk.Frame(root)
    tk.Label(verification_screen, text="Plik PDF:").pack(pady=5)
    tk.Button(verification_screen, text="Wybierz plik", command=select_file).pack(pady=5)
    tk.Button(verification_screen, text="Zweryfikuj podpis", command=verify_signature).pack(pady=5)
    
    return verification_screen

def navigation_view(root):
    nav_frame = tk.Frame(root)
    nav_frame.pack(pady=5)
    tk.Button(nav_frame, text="Podpisz dokument", command=show_signing_view).pack(side=tk.LEFT, padx=10)
    tk.Button(nav_frame, text="Zweryfikuj podpis", command=show_verification_view).pack(side=tk.LEFT, padx=10)

def monitor_usb():
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

root = tk.Tk()
root.title("BSK - Podpisywanie dokumentów")
root.geometry("450x450")

navigation_view(root)
signing_screen, entry_file, entry_pin = signing_view(root)
verification_screen = verification_view(root)
show_signing_view()

usb_thread = threading.Thread(target=monitor_usb, daemon=True)
usb_thread.start()

root.mainloop()
