import tkinter as tk
from datetime import datetime

def add_log(log_text, message):
    """
    @brief Dodaje komunikat do logu z aktualną datą i godziną.
    @param log_text: Widget tekstowy , do którego dodawany jest log.
    @param message: Treść komunikatu do zapisania w logu.
    """
    log_text.config(state=tk.NORMAL)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_with_timestamp = f"[{timestamp}] {message}"

    log_text.insert(tk.END, message_with_timestamp + "\n")
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)

def log_view(root):
    """
    @brief Tworzy okienko z historią wydarzeń występujących w aplikacji.
    @param root: Główne okno aplikacji.
    @return Zwraca widget tekstowy do wyświetlania i dodawania logów.
    """
    log_frame = tk.Frame(root)
    log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    tk.Label(log_frame, text="Logi:").pack(anchor=tk.W)
    log_text = tk.Text(log_frame, height=8, state=tk.DISABLED)
    log_text.pack(fill=tk.BOTH, expand=True)

    log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    return log_text
