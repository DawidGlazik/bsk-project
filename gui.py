import tkinter as tk
import threading
from tkinter import filedialog
import signFile
from logHistory import log_view, add_log
from usbDetector import *
from signFile import *
from verification import verify_signature


def select_file(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("Pliki PDF", "*.pdf")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)


def select_public_key(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("Pliki PEM", "*.pem")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

def sign_document():
    file_path = entry_file_signing.get()
    pin = entry_pin.get()
    if not file_path or not pin:
        add_log(log_text, "Błąd: Brak pliku PDF lub PIN-u.")
        return

    if not signFile.encrypted_pkey:
        add_log(log_text, "Błąd: Brak klucza prywatnego.")
        return

    decrypted_pkey = decrypt_key(pin)
    if decrypted_pkey is None:
        add_log(log_text, "Błąd: Nie udało się odszyfrować klucza prywatnego.")
        return

    hash_value = generate_hash(file_path)
    if hash_value is None:
        add_log(log_text, "Błąd: Nie udało się wygenerować skrótu pliku.")
        return

    signature = create_signature(hash_value, decrypted_pkey)
    if signature is None:
        add_log(log_text, "Błąd: Nie udało się stworzyć podpisu.")
        return

    if not bond_signature_and_pdf(file_path, signature):
        add_log(log_text, "Błąd: Nie udało się dołączyć podpisu do pliku PDF.")
        return

    add_log(log_text, "Sukces: Dokument podpisany.")


def verify_document():
    file_path = entry_file_verification.get()
    public_key_path = entry_public_key.get()

    if not file_path or not public_key_path:
        add_log(log_text, "Błąd: Brak pliku PDF lub klucza publicznego.")
        return

    result = verify_signature(file_path, public_key_path, log_text)
    if result:
        add_log(log_text, "Sukces: Podpis jest prawidłowy.")
    else:
        add_log(log_text, "Błąd: Podpis jest nieprawidłowy.")


def show_signing_view():
    verification_screen.pack_forget()
    signing_screen.pack(pady=10, fill=tk.BOTH, expand=True)


def show_verification_view():
    signing_screen.pack_forget()
    verification_screen.pack(pady=10, fill=tk.BOTH, expand=True)


def signing_view(root):
    signing_screen = tk.Frame(root)
    tk.Label(signing_screen, text="Plik PDF:").pack(pady=5)
    entry_file = tk.Entry(signing_screen, width=40)
    entry_file.pack()
    tk.Button(signing_screen, text="Wybierz plik", command=lambda: select_file(entry_file)).pack(pady=5)
    tk.Label(signing_screen, text="PIN:").pack(pady=5)
    entry_pin = tk.Entry(signing_screen, show="*", width=20)
    entry_pin.pack()
    tk.Button(signing_screen, text="Podpisz dokument", command=sign_document).pack(pady=10)
    return signing_screen, entry_file, entry_pin


def verification_view(root):
    verification_screen = tk.Frame(root)
    tk.Label(verification_screen, text="Plik PDF:").pack(pady=5)
    entry_file = tk.Entry(verification_screen, width=40)
    entry_file.pack()
    tk.Button(verification_screen, text="Wybierz plik", command=lambda: select_file(entry_file)).pack(pady=5)

    tk.Label(verification_screen, text="Klucz publiczny:").pack(pady=5)
    entry_key = tk.Entry(verification_screen, width=40)
    entry_key.pack()
    tk.Button(verification_screen, text="Wybierz certyfikat", command=lambda: select_public_key(entry_key)).pack(pady=5)

    tk.Button(verification_screen, text="Zweryfikuj podpis", command=verify_document).pack(pady=5)
    return verification_screen, entry_file, entry_key


def navigation_view(root):
    nav_frame = tk.Frame(root)
    nav_frame.pack(pady=5)
    tk.Button(nav_frame, text="Podpisz dokument", command=show_signing_view).pack(side=tk.LEFT, padx=10)
    tk.Button(nav_frame, text="Zweryfikuj podpis", command=show_verification_view).pack(side=tk.LEFT, padx=10)


root = tk.Tk()
root.title("BSK - Podpisywanie dokumentów")
root.geometry("450x500")

navigation_view(root)
signing_screen, entry_file_signing, entry_pin = signing_view(root)
verification_screen, entry_file_verification, entry_key = verification_view(root)
show_signing_view()

log_text = log_view(root)

usb_thread = threading.Thread(target=monitor_usb, args=(root, log_text), daemon=True)
usb_thread.start()

root.mainloop()
