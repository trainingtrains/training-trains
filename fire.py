import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database
conn = sqlite3.connect("internship.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    email TEXT,
    course TEXT
)
""")

conn.commit()

# Main Window
root = tk.Tk()
root.title("Training Trains Internship Management System")
root.geometry("900x600")

# Title
title = tk.Label(
    root,
    text="TRAINING TRAINS INTERNSHIP MANAGEMENT SYSTEM",
    font=("Arial",18,"bold")
)
title.pack(pady=10)

# Form Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame,text="Student Name").grid(row=0,column=0,padx=5,pady=5)
name_var = tk.StringVar()
tk.Entry(frame,textvariable=name_var,width=30).grid(row=0,column=1)

tk.Label(frame,text="Mobile").grid(row=1,column=0,padx=5,pady=5)
mobile_var = tk.StringVar()
tk.Entry(frame,textvariable=mobile_var,width=30).grid(row=1,column=1)

tk.Label(frame,text="Email").grid(row=2,column=0,padx=5,pady=5)
email_var = tk.StringVar()
tk.Entry(frame,textvariable=email_var,width=30).grid(row=2,column=1)

tk.Label(frame,text="Course").grid(row=3,column=0,padx=5,pady=5)

course_var = tk.StringVar()
course_combo = ttk.Combobox(
    frame,
    textvariable=course_var,
    values=[
        "Python",
        "Java",
        "Web Development",
        "Flutter",
        "AI & ML",
        "Cyber Security",
        "Data Science"
    ],
    width=27
)
course_combo.grid(row=3,column=1)

# TreeView
tree = ttk.Treeview(
    root,
    columns=("ID","Name","Mobile","Email","Course"),
    show="headings"
)

for col in ("ID","Name","Mobile","Email","Course"):
    tree.heading(col,text=col)

tree.pack(fill="both",expand=True,pady=10)

def load_students():
    tree.delete(*tree.get_children())

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("",tk.END,values=row)

def add_student():
    name = name_var.get()
    mobile = mobile_var.get()
    email = email_var.get()
    course = course_var.get()

    if not name:
        messagebox.showerror("Error","Enter Student Name")
        return

    cur.execute(
        "INSERT INTO students(name,mobile,email,course) VALUES(?,?,?,?)",
        (name,mobile,email,course)
    )

    conn.commit()

    load_students()

    name_var.set("")
    mobile_var.set("")
    email_var.set("")
    course_var.set("")

    messagebox.showinfo("Success","Student Added")

def delete_student():
    selected = tree.selection()

    if not selected:
        return

    item = tree.item(selected[0])

    student_id = item["values"][0]

    cur.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    conn.commit()

    load_students()

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(
    btn_frame,
    text="Add Student",
    bg="green",
    fg="white",
    command=add_student
).grid(row=0,column=0,padx=10)

tk.Button(
    btn_frame,
    text="Delete Student",
    bg="red",
    fg="white",
    command=delete_student
).grid(row=0,column=1,padx=10)

load_students()

root.mainloop()

conn.close()