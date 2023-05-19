import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip
import jieba
import re

DEFAULT_TOKEN_LIMIT = 3500

def split_text(text, token_limit):
    tokens = list(jieba.cut(text, cut_all=False))
    chunks = []
    chunk = []
    count = 0

    for token in tokens:
        count += len(token)
        if count <= token_limit:
            chunk.append(token)
        else:
            chunks.append(''.join(chunk))
            chunk = [token]
            count = len(token)
    
    if chunk:
        chunks.append(''.join(chunk))
    
    return chunks

def split_and_show():
    clear_buttons()
    input_text = input_box.get("1.0", tk.END)

    if input_text.strip() == "":
        messagebox.showerror("Error", "Please enter text")
        return

    token_limit = int(token_limit_entry.get())
    chunks = split_text(input_text, token_limit)
    for i, chunk in enumerate(chunks, start=1):
        btn = ttk.Button(button_frame, text=f"Copy Text Block {i}", command=lambda c=chunk: pyperclip.copy(c))
        btn.pack(fill=tk.X, padx=5, pady=5)
        buttons.append(btn)
    update_scrollregion()

def clear_text():
    input_box.delete("1.0", tk.END)

def clear_buttons():
    for btn in buttons:
        btn.pack_forget()
    buttons.clear()

def reset():
    clear_text()
    clear_buttons()
    token_limit_entry.delete(0, tk.END)
    token_limit_entry.insert(0, DEFAULT_TOKEN_LIMIT)

def update_scrollregion():
    button_canvas.update_idletasks()
    button_canvas.configure(scrollregion=button_canvas.bbox("all"))

def main():
    root = tk.Tk()
    root.title("Text Splitter")
    root.configure(bg='#A4C3B2')  # Update background color

    global input_box
    input_box = tk.Text(root, wrap=tk.WORD, height=20, width=80, bg='#E9F7EF')  # Update text box background color
    input_box.pack(padx=10, pady=10)

    control_frame = ttk.Frame(root, style='TFrame', padding=10)
    control_frame.pack(pady=10)

    split_button = ttk.Button(control_frame, text="Split", command=split_and_show)
    split_button.grid(row=0, column=0, padx=5)

    reset_button = ttk.Button(control_frame, text="Reset", command=reset)
    reset_button.grid(row=0, column=1, padx=5)

    token_limit_label = ttk.Label(control_frame, text="Token Limit:")
    token_limit_label.grid(row=0, column=2, padx=(20, 5))

    global token_limit_entry
    token_limit_entry = ttk.Entry(control_frame, width=8)
    token_limit_entry.insert(0, DEFAULT_TOKEN_LIMIT)
    token_limit_entry.grid(row=0, column=3)

    global button_canvas
    button_canvas = tk.Canvas(root, bg='#A4C3B2')  # Update canvas color
    button_canvas.pack(side=tk.LEFT, padx=(10, 0), pady=10)  # Adjust canvas margin

    global button_frame
    button_frame = ttk.Frame(button_canvas, style='TFrame')
    button_canvas.create_window((0, 0), window=button_frame, anchor=tk.NW)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=button_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    button_canvas.config(yscrollcommand=scrollbar.set)

    def on_configure(event):
        button_canvas.configure(scrollregion=button_canvas.bbox("all"))

    button_canvas.bind("<Configure>", on_configure)

    global buttons
    buttons = []

    root.mainloop()

if __name__ == "__main__":
    main()