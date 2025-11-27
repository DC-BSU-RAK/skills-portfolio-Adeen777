import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

#this is the file used to store student marks
FILENAME = "studentMarks.txt"

#this is to load all student data from the file
def load_data():
    students = []
    try:
        with open(FILENAME, "r") as f:
            lines = f.read().strip().split("\n")

            #this skip the first line
            for line in lines[1:]:
                parts = line.split(",")

                #this skip incomplete lines
                if len(parts) < 6:
                    continue

                #and this validate student code
                try:
                    code = int(parts[0])
                except:
                    continue

                name = parts[1]

                # this does intiger conversion of marks
                def safe_int(x):
                    try:
                        return int(x)
                    except:
                        return 0

                c1, c2, c3 = map(safe_int, parts[2:5])

                exam = safe_int(parts[5])

                students.append({
                    "code": code,
                    "name": name,
                    "coursework": [c1, c2, c3],
                    "exam": exam
                })

    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt not found.")

    return students

# this save the updated student data
def save_data(students):
    with open(FILENAME, "w") as f:
        f.write(str(len(students)) + "\n")
        for s in students:
            f.write(f"{s['code']},{s['name']},{s['coursework'][0]},"
                    f"{s['coursework'][1]},{s['coursework'][2]},{s['exam']}\n")

# this is to calculate coursework total percentage and grade
def calculate_results(s):
    total_coursework = sum(s['coursework'])
    total_marks = total_coursework + s['exam']

    #this is for course total marks and percentage
    percentage = (total_marks / 160) * 100

    #this is to determine grade
    if percentage >= 70:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    return total_coursework, s["exam"], percentage, grade

#this is for the table
def clear_display():
    """Clear all rows in the table."""
    for i in table.get_children():
        table.delete(i)


def display_students(students):
    """Insert student records into the table."""
    clear_display()

    for s in students:
        cw, exam, pct, grade = calculate_results(s)

        table.insert("", "end", values=(
            s["code"], s["name"], cw, exam, f"{pct:.1f}%", grade
        ))

#this is for menu
def view_all():
    """View all records."""
    students = load_data()
    if not students:
        return
    display_students(students)


def view_individual():
    """View a single student by code."""
    students = load_data()
    code = simpledialog.askstring("Search", "Enter student code:")

    if not code:
        return

    for s in students:
        if str(s["code"]) == code:
            display_students([s])
            return

    messagebox.showerror("Not Found", "Student does not exist.")


def show_highest():
    """Display student with highest total marks."""
    students = load_data()
    if not students:
        return

    best = max(students, key=lambda s: sum(s["coursework"]) + s["exam"])
    display_students([best])


def show_lowest():
    """Display student with lowest total marks."""
    students = load_data()
    if not students:
        return

    worst = min(students, key=lambda s: sum(s["coursework"]) + s["exam"])
    display_students([worst])


def sort_records():
    """Sort all records ascending or descending."""
    students = load_data()
    if not students:
        return

    ascending = messagebox.askyesno("Sort", "Sort ascending? (No = descending)")

    students.sort(key=lambda s: sum(s["coursework"]) + s["exam"],
                  reverse=not ascending)

    save_data(students)
    display_students(students)

#this is to add a new student
def add_record():
    """Open a form window to add a new student."""
    students = load_data()

    win = tk.Toplevel(root)
    win.title("Add New Student")
    win.geometry("350x400")

    tk.Label(win, text="Add New Student", font=("Arial", 16, "bold")).pack(pady=10)

    #this for code input
    tk.Label(win, text="Student Code:").pack()
    code_entry = tk.Entry(win)
    code_entry.pack()

    #this for name input
    tk.Label(win, text="Student Name:").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    #this for coursework inputs
    tk.Label(win, text="Coursework 1 (0–20):").pack()
    c1_entry = tk.Entry(win)
    c1_entry.pack()

    tk.Label(win, text="Coursework 2 (0–20):").pack()
    c2_entry = tk.Entry(win)
    c2_entry.pack()

    tk.Label(win, text="Coursework 3 (0–20):").pack()
    c3_entry = tk.Entry(win)
    c3_entry.pack()

    #this for the exam input
    tk.Label(win, text="Exam (0–100):").pack()
    exam_entry = tk.Entry(win)
    exam_entry.pack()

    def save_new_student():
        """Save student data after validation."""
        try:
            code = int(code_entry.get())
            name = name_entry.get()
            c1 = int(c1_entry.get())
            c2 = int(c2_entry.get())
            c3 = int(c3_entry.get())
            exam = int(exam_entry.get())
        except:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        students.append({
            "code": code,
            "name": name,
            "coursework": [c1, c2, c3],
            "exam": exam
        })

        save_data(students)
        view_all()
        win.destroy()
        messagebox.showinfo("Success", "Student added successfully!")

    tk.Button(win, text="Save Student", bg="#27ae60", fg="white",
              command=save_new_student).pack(pady=20)

#this is to delete records
def delete_record():
    """Delete a student using the student code."""
    students = load_data()
    code = simpledialog.askstring("Delete", "Enter student code:")

    new_list = [s for s in students if str(s["code"]) != code]

    if len(new_list) == len(students):
        messagebox.showerror("Error", "Student not found.")
        return

    save_data(new_list)
    view_all()

#this is to update a record
def update_record():
    """Open a window to update a student record."""
    students = load_data()
    code = simpledialog.askstring("Update", "Enter student code:")

    #this is to find student
    student = None
    for s in students:
        if str(s["code"]) == code:
            student = s
            break

    if not student:
        messagebox.showerror("Error", "Student not found.")
        return

    #this is to Update form
    win = tk.Toplevel(root)
    win.title("Update Student")
    win.geometry("350x400")

    tk.Label(win, text="Update Student Record", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(win, text="Name:").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()
    name_entry.insert(0, student["name"])

    tk.Label(win, text="Coursework 1 (0–20):").pack()
    cw1_entry = tk.Entry(win)
    cw1_entry.pack()
    cw1_entry.insert(0, student["coursework"][0])

    tk.Label(win, text="Coursework 2 (0–20):").pack()
    cw2_entry = tk.Entry(win)
    cw2_entry.pack()
    cw2_entry.insert(0, student["coursework"][1])

    tk.Label(win, text="Coursework 3 (0–20):").pack()
    cw3_entry = tk.Entry(win)
    cw3_entry.pack()
    cw3_entry.insert(0, student["coursework"][2])

    tk.Label(win, text="Exam (0–100):").pack()
    exam_entry = tk.Entry(win)
    exam_entry.pack()
    exam_entry.insert(0, student["exam"])

    def save_updates():
        """Apply updates to the selected student."""
        try:
            student["name"] = name_entry.get()
            student["coursework"][0] = int(cw1_entry.get())
            student["coursework"][1] = int(cw2_entry.get())
            student["coursework"][2] = int(cw3_entry.get())
            student["exam"] = int(exam_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Marks must be numbers!")
            return

        save_data(students)
        win.destroy()
        view_all()
        messagebox.showinfo("Success", "Record updated successfully!")

    tk.Button(win, text="Save Updates", bg="#4CAF50", fg="white",
              command=save_updates).pack(pady=20)

#this is the gui setup
root = tk.Tk()
root.title("Student Manager System")
root.geometry("900x500")
root.config(bg="#e6e6e6")

#this is for the menu panel
menu_frame = tk.Frame(root, bg="#313232", width=200)
menu_frame.pack(side="left", fill="y")

btn_style = {"bg": "#313232", "fg": "white",
             "font": ("Arial", 12), "bd": 0, "height": 2}

tk.Label(menu_frame, text="MENU", bg="#313232", fg="white",
         font=("Arial", 16, "bold")).pack(pady=10)

#menu buttons
tk.Button(menu_frame, text="View All Records", command=view_all, **btn_style).pack(fill="x")
tk.Button(menu_frame, text="View Individual", command=view_individual, **btn_style).pack(fill="x")
tk.Button(menu_frame, text="Highest Score", command=show_highest, **btn_style).pack(fill="x")
tk.Button(menu_frame, text="Lowest Score", command=show_lowest, **btn_style).pack(fill="x")
tk.Button(menu_frame, text="Sort Records", command=sort_records, **btn_style).pack(fill="x")
tk.Button(menu_frame, text="Add Record", command=add_record, **btn_style).pack(fill="x")
tk.Button(menu_frame, text="Delete Record", command=delete_record, **btn_style).pack(fill="x")
tk.Button(menu_frame, text="Update Record", command=update_record, **btn_style).pack(fill="x")

#this is for the table panel
display_frame = tk.Frame(root, bg="white")
display_frame.pack(side="right", fill="both", expand=True)

#for table columns
columns = ("Code", "Name", "Coursework", "Exam", "Percent", "Grade")
table = ttk.Treeview(display_frame, columns=columns, show="headings")
table.pack(fill="both", expand=True)

#this is to set table headers
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)

#this is for the scrollbar of the table
scroll = ttk.Scrollbar(display_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scroll.set)
scroll.pack(side="right", fill="y")

root.mainloop()