# Sara Carrasquillo
# 03-08-2025
# Here we have our frontend(graphical user interface) of our QR Code generator gui.py

#Imports
import os
import tkinter as tk
import pyperclipimg as pci
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk
from util import qr_size


class QRApp:
    def __init__(self, root):
        # Initializes the main application window
        self.root = root
        root.resizable(False, False)
        self.root.title("QR Generator")
        self.root.configure(bg="black")

        # Themed style
        style = ttk.Style()
        style.theme_use('clam')


        # UI element colors
        style.configure("TFrame", background="gray10")
        style.configure("TLabel", foreground="white", background="gray10")
        style.configure("TButton", foreground="white", background="black", bordercolor= "grey25")
        style.configure("TEntry", foreground="white", fieldbackground="black", background="black", bordercolor= "grey25")

        # Main frame with padding
        main_frame = ttk.Frame(root, padding="15")
        main_frame.grid(row=0, column=0, sticky="NSEW")

        # URL/Text Input Section
        ttk.Label(main_frame, text="URL/Text:").grid(row=0, column=0, sticky="e", padx=(0, 5), pady=5)
        self.data_entry = ttk.Entry(main_frame, width=40)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)

        # Size Input Section
        ttk.Label(main_frame, text="Size (px):").grid(row=1, column=0, sticky="e", padx=(0, 5), pady=5)
        self.size_entry = ttk.Entry(main_frame, width=10)
        self.size_entry.insert(0, "300")  # Default size to 300px
        self.size_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Generates Button Section
        generate_button = ttk.Button(main_frame, text="Generate", command=self.generate_qr)
        generate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # QR Code Preview Canvas Section standard canvas
        self.canvas = tk.Canvas(main_frame, width=300, height=300, bg="black", relief="sunken", borderwidth=1)
        self.canvas.grid(row=3, column=0, columnspan=2, pady=5)

        # Save Button Section
        self.save_btn = ttk.Button(main_frame, text="Save As...", command=self.save_qr, state="disabled")
        self.save_btn.grid(row=4, column=0, columnspan=2, pady=5)

        # Copy Button Section
        self.copy_btn = ttk.Button(main_frame, text="Copy", command=self.copy_qr, state="disabled" )
        self.copy_btn.grid(row=5, column=0, columnspan=2, pady=5)

        # Variables to store the generated image and its Tkinter-compatible format
        self.current_img = None
        self.tk_img = None

    # Generates QR code based on user input for the URL/text/size.
    def generate_qr(self):
        data = self.data_entry.get().strip()
        try:
            # Parse size from the entry and ensure that data is provided
            size = int(self.size_entry.get())
            if not data:
                raise ValueError("No data provided. Please enter a URL or text.")
        except Exception as e:
            messagebox.showerror("Input Error", str(e))
            return

        # Generates QR code image with the given data and size
        img = qr_size(data, size)
        self.current_img = img

        # Converts PIL image to a format that works in Tkinter
        self.tk_img = ImageTk.PhotoImage(img)

        # Updates canvas dimensions and display the new QR code image
        self.canvas.config(width=size, height=size)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        # Enables save/copy button once image is generated
        self.save_btn.config(state="normal")
        self.copy_btn.config(state="normal")

    # Function to copy the qr code cross-platform via pyperclipimg
    def copy_qr(self):
        pci.copy(self.current_img)  # Copy PIL.Image to clipboard
        messagebox.showinfo("Copied", "Copied to clipboard.")

    # Function to save the qr in multiple formats
    def save_qr(self):
        if self.current_img:
            # Defines types of files that can be saved
            file_types = [
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg;*.jpeg"),
                ("GIF Image", "*.gif"),
                ("BMP Image", "*.bmp"),
                ("All Files", "*.*")
            ]
            # Opens save dialog
            file_path = asksaveasfilename(
                defaultextension=".png",
                filetypes=file_types,
                title="Save QR Code As..."
            )
            if file_path:
                try:
                    # Gets lower-case file extension
                    ext = os.path.splitext(file_path)[1].lower()

                    img_to_save = self.current_img
                    # Converts image (if necessary) based on extension
                    if ext in [".jpg", ".jpeg", ".bmp"]:
                        if img_to_save.mode != "RGB":
                            img_to_save = img_to_save.convert("RGB")
                    elif ext == ".gif":
                        pass

                    # Saves the image using Pillow
                    img_to_save.save(file_path)
                    print(f"Image saved as {file_path}")
                except Exception as e:
                    print("Error saving image:", e)