from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter
from tkinter import messagebox
import os


encrypted_pkey = None


def load_key(usb_path):
    global encrypted_pkey

    try:
        files = [f for f in os.listdir(usb_path) if f.endswith('.enc')]

        if len(files) == 1:
            key_path = os.path.join(usb_path, files[0])
            with open(key_path, "rb") as f:
                encrypted_pkey = f.read()
                print("signFile",encrypted_pkey)
            messagebox.showinfo("Sukces", "Klucz prywatny został załadowany.")
        else:
            messagebox.showerror("Błąd", "Nie odnaleziono klucza prywatnego lub odnaleziono jego wiele instancji.")
            return None

    except Exception as e:
        messagebox.showerror("Błąd", "Nie udało się załadować klucza prywatnego z usb.")
        return None


def verify_signature(file_path, public_key_path):
    try:
        # Wczytanie klucza publicznego
        with open(public_key_path, "rb") as f:
            public_key = RSA.import_key(f.read())

        # Odczytanie dokumentu PDF
        reader = PdfReader(file_path)
        metadata = reader.metadata

        # Pobranie podpisu z metadanych
        hex_signature = metadata.get("/Podpis")
        if not hex_signature:
            messagebox.showerror("Błąd", "Brak podpisu w pliku PDF.")
            return False

        signature = bytes.fromhex(hex_signature)

        # Wygenerowanie hash pliku
        hash = SHA256.new()
        with open(file_path, "rb") as pdf:
            hash.update(pdf.read())

        # Weryfikacja podpisu
        try:
            print(public_key)
            pkcs1_15.new(public_key).verify(hash, signature)
            messagebox.showinfo("Sukces", "Podpis jest poprawny.")
            return True
        except (ValueError, TypeError):
            messagebox.showerror("Błąd", "Podpis nie jest prawidłowy.")
            return False
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas weryfikacji: {str(e)}")
        return False


def decrypt_key(pin):
    global encrypted_pkey
    try:
        aes = SHA256.new(pin.encode()).digest()

        nonce = encrypted_pkey[:16]
        tag = encrypted_pkey[16:32]
        rest = encrypted_pkey[32:]

        secret = AES.new(aes, AES.MODE_EAX, nonce=nonce)
        decrypted_pkey = secret.decrypt_and_verify(rest, tag)

        return RSA.import_key(decrypted_pkey)

    except (ValueError, KeyError):
        messagebox.showerror("Błąd", "Nie udało się odszyfrować klucza prywatnego.")
        return None


def generate_hash(file_path):
    try:
        hash = SHA256.new()

        with open(file_path, "rb") as pdf:
            data = pdf.read()
            hash.update(data)
        return hash

    except Exception as e:
        messagebox.showerror("Błąd", "Nie udało się wygenerować hash'a pliku pdf.")
        return None


def create_signature(hash, decrypted_pkey):
    try:
        return pkcs1_15.new(decrypted_pkey).sign(hash)

    except Exception as e:
        messagebox.showerror("Błąd", "Nie udało się podpisać pliku.")
        return None


def bond_signature_and_pdf(file_path, signature):
    try:
        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        hex_signature = signature.hex()
        writer.add_metadata({"/Podpisane przez": "Użytkownik A", "/Podpis": hex_signature})

        with open(file_path, "wb") as signed:
            writer.write(signed)

        messagebox.showinfo("Sukces", "Podpisano plik pomyślnie.")
        return file_path

    except Exception as e:
        messagebox.showerror("Błąd", "Nie udało się umieścić podpisu w metadanych pliku.")
        return None