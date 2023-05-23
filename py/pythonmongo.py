import pymongo
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Connect to MongoDB Atlas cluster
client = pymongo.MongoClient("mongodb+srv://chauhan:vishal@cluster0.nsbsrbo.mongodb.net/?retryWrites=true&w=majority")
db = client["ads1"]
collection = db["ads"]

# Create the GUI window
window = tk.Tk()
window.title("MongoDB CRUD Operations")
window.geometry("500x400")
window.configure(bg='orange')

# Function to display data from the database
def display_data():
    result = collection.find()
    for i in tree.get_children():
        tree.delete(i)
    for row in result:
        tree.insert("", "end", values=(row['_id'], row['name'], row['address']))

# Function to add a new record to the database
def add_record():
    name = name_entry.get()
    address = address_entry.get()
    if not name or not address:
        messagebox.showerror("Error", "Name and address fields cannot be empty!")
        return
    new_record = {"name": name, "address": address}
    collection.insert_one(new_record)
    display_data()
    name_entry.delete(0, "end")
    address_entry.delete(0, "end")

# Function to update an existing record in the database
def update_record():
    name = name_entry.get()
    address = address_entry.get()
    if not name or not address:
        messagebox.showerror("Error", "Name and address fields cannot be empty!")
        return
    filter_query = {"name": name}
    update_query = {"$set": {"address": address}}
    result = collection.update_one(filter_query, update_query)
    if result.matched_count == 0:
        messagebox.showwarning("Warning", "No record found with the given name!")
    display_data()
    name_entry.delete(0, "end")
    address_entry.delete(0, "end")

# Function to delete a record from the database
def delete_record():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Error", "Name field cannot be empty!")
        return
    filter_query = {"name": name}
    result = collection.delete_one(filter_query)
    if result.deleted_count == 0:
        messagebox.showwarning("Warning", "No record found with the given name!")
    display_data()
    name_entry.delete(0, "end")
    address_entry.delete(0, "end")

# Create the treeview to display the data
tree = ttk.Treeview(window, columns=("ID", "Name", "Address"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Address", text="Address")
tree.pack(padx=20, pady=(20, 10))

# Create the input fields and buttons
input_frame = tk.Frame(window, bg="#F0F0F0", pady=10)
input_frame.pack()

name_label = tk.Label(input_frame, text="Name", bg="#F0F0F0")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

address_label = tk.Label(input_frame, text="Address", bg="#F0F0F0")
address_label.grid(row=1, column=0, padx=5, pady=5)
address_entry = tk.Entry(input_frame, width=30)
address_entry.grid(row=1, column=1, padx=5, pady=5)

button_frame = tk.Frame(window, bg="orange")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add", bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5, bd=0, command=add_record)
add_button.pack(side=tk.LEFT, padx=5)

update_button = tk.Button(button_frame, text="Update", bg="blue", fg="white", font=("Arial", 12), padx=10, pady=5, bd=0, command=update_record)
update_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Delete", bg="#F44336", fg="white", font=("Arial", 12), padx=10, pady=5, bd=0, command=delete_record)
delete_button.pack(side=tk.LEFT, padx=5)

display_button = tk.Button(button_frame, text="Display Data", bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5, bd=0, command=display_data)
display_button.pack(side=tk.RIGHT, padx=5)

# Styling the input fields
style = ttk.Style()
style.configure("TEntry", font=("Arial", 12), padding=5)

# Run the GUI
window.mainloop()

# Close the cursor and database connection
# mycursor.close()
# mydb.close()