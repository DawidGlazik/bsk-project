import tkinter as tk
from tkinter.scrolledtext import ScrolledText


def add_log(log_text,message):
    log_text.config(state=tk.NORMAL)

    log_text.insert(tk.END, message + "\n")
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)


def log_view(root):
    log_frame = tk.Frame(root)
    log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    tk.Label(log_frame, text="Logi:").pack(anchor=tk.W)
    log_text = tk.Text(log_frame, height=8, state=tk.DISABLED)
    log_text.pack(fill=tk.BOTH, expand=True)

    log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    return log_text