import tkinter as tk
from tkinter import messagebox
import random
import os

#Joke app

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Assistant")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        self.root.config(bg="#1E1E1E")   #this is for the dark background

#this is to load jokes from the file
        self.jokes = self.load_jokes()

#this is to store current joke parts
        self.current_setup = ""
        self.current_punchline = ""

#this is for the title
        self.title_label = tk.Label(
            root,
            text="😂 Alexa Joke Assistant 😂",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1E1E1E"
        )
        self.title_label.pack(pady=10)

#this is for the joke label
        self.setup_label = tk.Label(
            root,
            text="Click a button to start!",
            font=("Arial", 14),
            fg="#FFD700",
            bg="#1E1E1E",
            wraplength=450,
            justify="center"
        )
        self.setup_label.pack(pady=10)

#this is for the punchline label
        self.punchline_label = tk.Label(
            root,
            text="",
            font=("Arial", 14, "italic"),
            fg="#ADFF2F",
            bg="#1E1E1E",
            wraplength=450,
            justify="center"
        )
        self.punchline_label.pack(pady=10)

#this is for the frame of the buttons
        btn_frame = tk.Frame(root, bg="#1E1E1E")
        btn_frame.pack(pady=15)

#this is for the main buttons
        self.create_button(btn_frame, "Alexa tell me a Joke", self.show_joke).grid(row=0, column=0, padx=5)
        self.create_button(btn_frame, "Show Punchline", self.show_punchline).grid(row=0, column=1, padx=5)
        self.create_button(btn_frame, "Next Joke", self.show_joke).grid(row=1, column=0, padx=5, pady=5)
        self.create_button(btn_frame, "Quit", root.quit).grid(row=1, column=1, padx=5, pady=5)

 #this is to style the buttons
    def create_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            bg="#0078FF",
            fg="white",
            activebackground="#005FCC",
            width=15,
            height=1
        )

#this is to load jokes from text file
    def load_jokes(self):
        try:
            file_path = os.path.join("exercise-2 - alexa tell me a joke", "randomJokes.txt")
            
            with open(file_path, "r", encoding="utf-8") as f:
                jokes = [line.strip() for line in f.readlines() if "?" in line]

            return jokes

        except FileNotFoundError:
            messagebox.showerror("Error", "randomJokes.txt not found in resources folder!")
            return []

 #this is to pick and display new jokes
    def show_joke(self):
        if not self.jokes:
            return
        
        joke = random.choice(self.jokes)

#this is to split joke into setup and punchline
        setup, punchline = joke.split("?", 1)

        self.current_setup = setup + "?"
        self.current_punchline = punchline
        self.setup_label.config(text=self.current_setup)
        self.punchline_label.config(text="")

#this is to show the punch line
    def show_punchline(self):
        self.punchline_label.config(text=self.current_punchline)

if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()