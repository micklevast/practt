# program to perform CRUD operations on MySQL database using Python
from tkinter import ttk
import tkinter as tk
import mysql.connector as mysql
from tkinter import messagebox as mb

# connect to database
db = mysql.connect(
    host="localhost",
    user="root",
    password="Vishal@20",
    database="vishal"
)

# create cursor
cursor = db.cursor()

# def the functions
# configure the database


def configure_db():
    cursor.execute("CREATE DATABASE IF NOT EXISTS quiz")
    cursor.execute("USE quiz")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS ads (id INT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
    db.commit()
    mb.showinfo("Success", "Database configured successfully")


# create the gui
root = tk.Tk()
root.title("MySQL CRUD GUI")
root.geometry("700x500")


# Create the labels
label_id = tk.Label(root, text="ID")
label_name = tk.Label(root, text="Name")
label_email = tk.Label(root, text="Email")

# Create the entries
entry_id = tk.Entry(root)
entry_name = tk.Entry(root)
entry_email = tk.Entry(root)


def add_record():
    # get data from entries
    id = entry_id.get()
    name = entry_name.get()
    email = entry_email.get()

    # validate data
    if id == "" or name == "" or email == "":
        mb.showinfo("Error", "Please fill all the fields")
        return
    # verify if the id is unique
    cursor.execute("SELECT * FROM ads WHERE id = %s", (id,))
    record = cursor.fetchone()
    if record != None:
        mb.showinfo("Error", "ID already exists")
        return
    # verify email format
    if not email.endswith("@gmail.com"):
        mb.showinfo("Error", "Invalid email")
        return

    try:
        # Insert the record into the database
        cursor.execute(
            "INSERT INTO ads (id, name, email) VALUES (%s, %s, %s)", (id, name, email))
        db.commit()
        show_records_tree()
        mb.showinfo("Success", "Record inserted successfully")
    except:
        db.rollback()
        mb.showinfo("Error", "Could not insert record")


def update_record():
    # get data from entries
    id = entry_id.get()
    name = entry_name.get()
    email = entry_email.get()

    # validate data
    if id == "" or name == "" or email == "":
        mb.showinfo("Error", "Please fill all the fields")
        return
    # verify if the id is unique
    cursor.execute("SELECT * FROM ads WHERE id = %s", (id,))
    record = cursor.fetchone()
    if record == None:
        mb.showinfo("Error", "ID does not exist")
        return
    # verify email format
    if not email.endswith("@gmail.com"):
        mb.showinfo("Error", "Invalid email")
        return

    try:
        # Update the record into the database
        cursor.execute(
            "UPDATE ads SET name = %s, email = %s WHERE id = %s", (name, email, id))
        db.commit()
        show_records_tree()
        mb.showinfo("Success", "Record updated successfully")
    except:
        db.rollback()
        mb.showinfo("Error", "Could not update record")


def delete_record():
    # get data from entries
    id = entry_id.get()

    # validate data
    if id == "":
        mb.showinfo("Error", "Please fill all the fields")
        return
    # verify if the id is unique
    cursor.execute("SELECT * FROM ads WHERE id = %s", (id,))
    record = cursor.fetchone()
    if record == None:
        mb.showinfo("Error", "ID does not exist")
        return

    try:
        # Delete the record from the database
        cursor.execute("DELETE FROM ads WHERE id = %s", (id,))
        db.commit()
        show_records_tree()
        mb.showinfo("Success", "Record deleted successfully")
    except:
        db.rollback()
        mb.showinfo("Error", "Could not delete record")


# Create the buttons
button_add = tk.Button(root, text="Add", command=add_record)
button_update = tk.Button(root, text="Update", command=update_record)
button_delete = tk.Button(root, text="Delete", command=delete_record)

# change color of the buttons
button_add.config(bg="green", fg="white")
button_update.config(bg="blue", fg="white")
button_delete.config(bg="red", fg="white")

# change color of the labels
label_id.config(bg="lightblue", fg="black")
label_name.config(bg="lightblue", fg="black")
label_email.config(bg="lightblue", fg="black")

# change color of the entries
entry_id.config(bg="lightgreen", fg="black")
entry_name.config(bg="lightgreen", fg="black")
entry_email.config(bg="lightgreen", fg="black")

# change color of the root window
root.config(bg="lightblue")


# layout the gui
label_id.grid(row=0, column=0)
label_name.grid(row=1, column=0)
label_email.grid(row=2, column=0)
entry_id.grid(row=0, column=1)
entry_name.grid(row=1, column=1)
entry_email.grid(row=2, column=1)
button_add.grid(row=3, column=0)
button_update.grid(row=3, column=1)
button_delete.grid(row=3, column=2)

# add configure db button
button_configure = tk.Button(root, text="Configure DB", command=configure_db)
button_configure.grid(row=4, column=0)

# show records in a treeview
tree = ttk.Treeview(root)
tree["columns"] = ("one", "two", "three")
tree.column("one", width=60)
tree.column("two", width=100)
tree.column("three", width=200)
tree.heading("one", text="ID")
tree.heading("two", text="Name")
tree.heading("three", text="Email")
tree.grid(row=5, column=0, columnspan=3)


def show_records_tree():
    cursor.execute("SELECT * FROM ads")
    records = cursor.fetchall()
    # clear the treeview
    tree.delete(*tree.get_children())
    # insert records into the treeview
    for record in records:
        tree.insert("", tk.END, text="Record", values=record)
    # mb.showinfo("Records", records)


button_show_tree = tk.Button(
    root, text="Show Records Tree", command=show_records_tree)
button_show_tree.grid(row=4, column=2)


# main loop
root.mainloop()
show_records_tree()

# close the cursor object
cursor.close()

# close the database connection
db.close()
