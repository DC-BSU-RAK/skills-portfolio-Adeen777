import tkinter as tk
from tkinter import messagebox
import random

# This is the coloring for every botton,card and background for the quiz
BG_COLOR = "#028700"
CARD_COLOR = "#ffffff"
BTN_COLOR = "#0077ff"
BTN_TEXT = "white"
FONT_MAIN = ("Arial", 16)
FONT_TITLE = ("Arial", 20, "bold")

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        # FIX: Changed .heading() to the correct method, .title(), for the main window
        self.root.title("Math Quiz")
        self.root.geometry("500x380")
        self.root.configure(bg=BG_COLOR)
    #this is for tracking the score        
        self.score = 0
        self.question_count = 0
        self.present_answer = None
        self.attempt = 1
        self.difficulty = None
#this is for showing menu
        self.Make_menu()

    def clear(self):
        # FIX: The correct method to get all child widgets is winfo_children()
        for widget in self.root.winfo_children():
            widget.destroy()

#this is the starting page where you select the difficulty
    def Make_menu(self):
        self.clear()

        frame = tk.Frame(self.root, bg=CARD_COLOR, padx=20, pady=20, bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        title = tk.Label(frame, text="Difficulty level", font=FONT_TITLE, bg=CARD_COLOR)
        title.pack(pady=(0, 20))
        tk.Button(
            frame, text="Easy", bg=BTN_COLOR, fg=BTN_TEXT, font=FONT_MAIN,
            command=lambda: self.start_quiz("easy")
        ).pack(fill="x", pady=5)
        tk.Button(
            frame, text="Medium", bg=BTN_COLOR, fg=BTN_TEXT, font=FONT_MAIN,
            command=lambda: self.start_quiz("medium")
        ).pack(fill="x", pady=5)
        tk.Button(
            frame, text="hard", bg=BTN_COLOR, fg=BTN_TEXT, font=FONT_MAIN,
            command=lambda: self.start_quiz("hard")
        ).pack(fill="x", pady=5)

# Starting quiz after selecting difficulty
    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.question_count = 0
        self.next_question()

#this is to generate randome number and operators to ask questions based on the difficulty user chose
    def randomInt(self):
        if self.difficulty == "easy":
            return random.randint(1, 9)
        elif self.difficulty == "medium":
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def decideOperation(self):
        return random.choice(["+", "-"])

#this is for the page where they are asked questions
    def next_question(self):
        if self.question_count >= 10:
            self.display_results()
            return

        self.clear()
        self.attempt = 1
        self.question_count += 1
        num1 = self.randomInt()
        num2 = self.randomInt()
        op = self.decideOperation()

#checking correct answer
        if op == "+":
            self.present_answer = num1 + num2
        else:
            self.present_answer = num1 - num2

#making questions card
        frame = tk.Frame(self.root, bg=CARD_COLOR, padx=20, pady=20, bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        label = tk.Label(frame, text=f"Question {self.question_count}/10", font=FONT_MAIN, bg=CARD_COLOR)
        label.pack(pady=5)
        self.problem_label = tk.Label(
            frame, text=f"{num1} {op} {num2} =", font=FONT_TITLE, bg=CARD_COLOR
        )
        self.problem_label.pack(pady=10)
        self.answer_entry = tk.Entry(frame, font=FONT_MAIN)
        self.answer_entry.pack(pady=10)
        submit_btn = tk.Button(
            frame, text="Submit", font=FONT_MAIN, bg=BTN_COLOR, fg=BTN_TEXT,
            command=self.check_answer
        )
        submit_btn.pack(pady=5)

    #thid is to check users answer and give score based on the answer 1st time or 2nd time.
    def check_answer(self):
        user_input = self.answer_entry.get().strip()

        # Check for valid integer input (including negative numbers)
        is_integer = False
        try:
            int(user_input)
            is_integer = True
        except ValueError:
            pass
            
        if not is_integer:
            # Added a title to the messagebox and passed the root object
            messagebox.showwarning("Invalid Input", "Please enter a whole number.", parent=self.root)
            return

        user_answer = int(user_input)
        if user_answer == self.present_answer:
            if self.attempt == 1:
                self.score += 10
            else:
                self.score += 5
            messagebox.showinfo("Correct!", "You got it right!", parent=self.root)
            self.next_question()

        else:
            if self.attempt == 1:
                messagebox.showinfo("Try Again", "Incorrect answer. You have one more attempt.", parent=self.root)
                self.attempt = 2
            else:
                messagebox.showinfo(
                    "Incorrect",
                    f"Incorrect again. The correct answer was {self.present_answer}.",
                    parent=self.root
                )
                self.next_question()

#this is for result page
    def display_results(self):
        self.clear()
        grade = self.calculate_grade(self.score)
        frame = tk.Frame(self.root, bg=CARD_COLOR, padx=20, pady=20, bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Quiz Finished!", font=FONT_TITLE, bg=CARD_COLOR).pack(pady=10)
        tk.Label(frame, text=f"Score: {self.score}/100", font=FONT_MAIN, bg=CARD_COLOR).pack(pady=5)
        tk.Label(frame, text=f"Grade: {grade}", font=FONT_MAIN, bg=CARD_COLOR).pack(pady=5)
        tk.Button(
            frame, text="Play Again", bg=BTN_COLOR, fg=BTN_TEXT, font=FONT_MAIN,
            command=self.Make_menu
        ).pack(fill="x", pady=10)
        tk.Button(
            frame, text="Exit", bg="red", fg="white", font=FONT_MAIN,
            command=self.root.quit
        ).pack(fill="x")

    #this calculate your total score and grade you
    def calculate_grade(self, score):
        if score >= 90: return "A+"
        if score >= 80: return "A"
        if score >= 70: return "B"
        if score >= 60: return "C"
        return "D"

root = tk.Tk()
app = ArithmeticQuiz(root)
root.mainloop()