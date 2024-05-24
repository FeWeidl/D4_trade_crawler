import tkinter as tk
from tkinter import scrolledtext
from tkinter import font as tkfont
from PIL import Image, ImageTk
import threading
import logging
from start_crawler import start_crawler, stop_crawler

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.yview(tk.END)

class CrawlerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crawler Control")
        self.root.geometry("1600x900")  # Set the window size for a larger widescreen format

        self.running = False

        # Load and display the background image
        self.load_background()

        # Create a frame for the buttons with a black background
        self.button_frame = tk.Frame(root, bg="black", highlightthickness=0)
        self.button_frame.pack(side=tk.TOP, pady=20)

        # Create buttons with enhanced styling
        button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.start_button = tk.Button(self.button_frame, text="Start", width=15, command=self.start_thread, bg="#4CAF50", fg="white", font=button_font, activebackground="#45a049", bd=0)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop", width=15, command=self.stop_crawler, bg="#f44336", fg="white", font=button_font, activebackground="#e41e26", bd=0)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.exit_button = tk.Button(self.button_frame, text="Exit", width=15, command=self.exit_app, bg="#555555", fg="white", font=button_font, activebackground="#444444", bd=0)
        self.exit_button.grid(row=0, column=2, padx=10)

        # Create a scrolled text widget for logs with a themed appearance
        self.log_area = scrolledtext.ScrolledText(root, width=180, height=15, state=tk.DISABLED, bg="#2C0E0E", fg="#E5E5E5", font=("Courier New", 10))
        self.log_area.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 20))  # Move log area to the bottom and make it resizable

        # Set up logging to the text widget
        text_handler = TextHandler(self.log_area)
        logging.basicConfig(level=logging.INFO, handlers=[text_handler], format='%(asctime)s - %(levelname)s - %(message)s')

    def load_background(self):
        # Load the image file
        bg_image = Image.open("background.png")
        bg_image = bg_image.resize((1600, 900), Image.LANCZOS)  # Resize the image to fit the GUI
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Create a label to display the image
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def start_thread(self):
        if not self.running:
            self.running = True
            logging.info("Crawler started...")
            self.thread = threading.Thread(target=self.start_crawler_wrapper)
            self.thread.start()

    def start_crawler_wrapper(self):
        start_crawler()

    def stop_crawler(self):
        if self.running:
            stop_crawler()
            self.running = False
            logging.info("Crawler stopped...")

    def exit_app(self):
        self.stop_crawler()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CrawlerGUI(root)
    root.mainloop()
