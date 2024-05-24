import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import threading
from start_crawler import start_crawler, stop_crawler

class CrawlerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crawler Control")
        self.root.geometry("800x600")  # Set the window size

        self.running = False

        # Create a frame for the buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        # Create buttons
        self.start_button = tk.Button(self.button_frame, text="Start", width=15, command=self.start_thread)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop", width=15, command=self.stop_crawler)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.exit_button = tk.Button(self.button_frame, text="Exit", width=15, command=self.exit_app)
        self.exit_button.grid(row=0, column=2, padx=10)

        # Create a scrolled text widget for logs
        self.log_area = scrolledtext.ScrolledText(root, width=90, height=30)
        self.log_area.pack(pady=20)

    def start_thread(self):
        if not self.running:
            self.running = True
            self.log_area.insert(tk.END, "Crawler started...\n")
            self.thread = threading.Thread(target=self.start_crawler_wrapper)
            self.thread.start()

    def start_crawler_wrapper(self):
        start_crawler()

    def stop_crawler(self):
        if self.running:
            stop_crawler()
            self.running = False
            self.log_area.insert(tk.END, "Crawler stopped...\n")

    def exit_app(self):
        self.stop_crawler()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CrawlerGUI(root)
    root.mainloop()
