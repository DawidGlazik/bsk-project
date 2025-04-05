import tkinter as tk
from tkinter import messagebox, filedialog
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
import os


def save_key(pub_key):
    """
    @brief Zapisuje klucz publiczny do pliku PEM.
    @param pub_key: Klucz publiczny do zapisania.
    """
    path = filedialog.asksaveasfilename(defaultextension=".pem", title="Zapisz klucz publiczny")
    if path:
        with open(path, 'wb') as f:
            f.write(pub_key)
    else:
        messagebox.showerror("Błąd", "Nie wybrano ścieżki.")


def save_on_usb(aes, priv_key):
    """
    @brief Zapisuje zaszyfrowany klucz prywatny na USB.
    @param aes: Klucz AES do szyfrowania.
    @param priv_key: Klucz prywatny do zapisania.
    """
    secret = AES.new(aes, AES.MODE_EAX)
    keyToText, tag = secret.encrypt_and_digest(priv_key)

    path = filedialog.askdirectory(title="Wybierz docelowy USB")
    if path:
        key_path = os.path.join(path, "priv_key.enc")
        with open(key_path, 'wb') as f:
            f.write(secret.nonce + tag + keyToText)
        messagebox.showinfo("Sukces", "Zapisano klucz prywatny.")
    else:
        messagebox.showerror("Błąd", "Nie wybrano USB.")


def gen_keys():
    """
    @brief Generuje parę kluczy RSA i zapisuje je.
    @details Funkcja pobiera PIN z pola tekstowego, generuje klucze RSA, 
    szyfruje klucz prywatny, zapisuje klucz publiczny lokalnie oraz prywatny na USB.
    """
    pin = pin_entry.get()
    if not pin:
        messagebox.showerror("Błąd", "Nie podano PINu.")
        return

    key = RSA.generate(4096)
    priv_key = key.export_key()
    pub_key = key.publickey().export_key()
    aes = SHA256.new(pin.encode()).digest()
    save_key(pub_key)
    save_on_usb(aes, priv_key)


root = tk.Tk()
root.title("Generator kluczy RSA")
root.geometry("400x250")

tk.Label(root, text="PIN:").pack(pady=5)
pin_entry = tk.Entry(root, show="*", width=20)
pin_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generuj klucze", command=gen_keys)
generate_button.pack(pady=10)

root.mainloop()
