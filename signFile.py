from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter
from tkinter import messagebox
import os

from logHistory import add_log

encrypted_pkey = None


def load_key(usb_path, log_text):
    global encrypted_pkey

    try:
        files = [f for f in os.listdir(usb_path) if f.endswith('.enc')]

        if len(files) == 1:
            key_path = os.path.join(usb_path, files[0])
            with open(key_path, "rb") as f:
                encrypted_pkey = f.read()
                add_log(log_text, "Załadowano klucz prywatny z usb.")
        else:
            add_log(log_text, "Błąd: Brak klucza prywatnego na usb lub więcej niż jeden klucz.")
            return None

    except Exception as e:
        add_log(log_text, "Błąd: Nie udało się załadować klucza prywatnego.")
        return None



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
        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        temporary_file = "temporary_file.pdf"
        with open(temporary_file, "wb") as temp_file:
            writer.write(temp_file)

        with open(temporary_file, "rb") as pdf:
            data = pdf.read()
            hash.update(data)

        os.remove(temporary_file)
        return hash
    except Exception as e:
        return None


def create_signature(hash, decrypted_pkey):
    try:
        return pkcs1_15.new(decrypted_pkey).sign(hash)

    except Exception as e:
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

        return file_path

    except Exception as e:
        return None
