import tkinter as tk
from pymongo import MongoClient

def fetch_data():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://krishna:book@cluster0.nsbsrbo.mongodb.net/?retryWrites=true&w=majority')

    # Access the database and collection
    db = client['ads9']
    collection = db['customers']

    # Fetch data from the collection
    data = collection.find()

    # Display the data in the GUI
    for idx, record in enumerate(data):
        id_label = tk.Label(root, text=f"ID: {record['_id']}")
        id_label.grid(row=idx+2, column=0)

        name_label = tk.Label(root, text=f"Name: {record['name']}")
        name_label.grid(row=idx+2, column=1)

        email_label = tk.Label(root, text=f"Email: {record['email']}")
        email_label.grid(row=idx+2, column=2)

# Create the GUI window
root = tk.Tk()
root.title("MongoDB Records")
root.geometry("400x300")

# Fetch and display data button
fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=1, column=1)

# Labels for column headers
id_header = tk.Label(root, text="ID")
id_header.grid(row=2, column=0)

name_header = tk.Label(root, text="Name")
name_header.grid(row=2, column=1)

email_header = tk.Label(root, text="Email")
email_header.grid(row=2, column=2)

# Start the GUI event loop
root.mainloop()
