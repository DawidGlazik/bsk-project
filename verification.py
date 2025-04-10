import binascii
from tkinter import messagebox

from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from PyPDF2 import PdfReader

from logHistory import add_log
from signFile import generate_hash

def extract_signature(file_path):
    """
    @brief Wyodrębnia podpis z metadanych pliku PDF.
    @param file_path: Ścieżka do pliku PDF.
    @return Podpis w postaci bajtów, jeśli istnieje; inaczej None.
    """
    try:
        reader = PdfReader(file_path)
        metadata = reader.metadata

        if metadata and "/Podpis" in metadata:
            hex_signature = metadata["/Podpis"]
            return bytes.fromhex(hex_signature)
        else:
            return None
    except Exception as e:
        return None

def verify_signature(file_path, public_key_path, log_text):
    """
    @brief Weryfikuje podpis cyfrowy dokumentu PDF.
    @param file_path: Ścieżka do pliku PDF.
    @param public_key_path: Ścieżka do klucza publicznego.
    @param log_text: Widget tekstowy logów do wyświetlania komunikatów.
    @return True Jeśli podpis jest poprawny. False w przeciwnym razie.
    """
    try:
        signature = extract_signature(file_path)
        if signature is None:
            return False

        hash_value = generate_hash(file_path)
        if hash_value is None:
            return False

        with open(public_key_path, "rb") as key_file:
            public_key = RSA.import_key(key_file.read())

        try:
            pkcs1_15.new(public_key).verify(hash_value, signature)
            return True
        except (ValueError, TypeError):
            return False
    except Exception as e:
        add_log(log_text, "Błąd: Nie udało się zweryfikować podpisu.")
        return False
