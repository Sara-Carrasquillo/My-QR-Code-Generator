# Sara Carrasquillo
# 03-08-2025
# Here we have our execution file(main) of our QR Code generator main.py

# Imports Tkinter for the GUI
import tkinter as tk
# Imports the QRApp class
from gui import QRApp

def main():
    # Creates the main window
    root = tk.Tk()
    # Initializes the QRApp interface
    QRApp(root)
    # Starts the Tkinter event loop
    root.mainloop()
# This runs the main function
if __name__ == "__main__":
    main()
