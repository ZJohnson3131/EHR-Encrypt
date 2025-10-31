#TODO
# Build landing screen for GUI and link button functions to backend
# Need to include buttons for login, change password and exit
# Once logged in, create new options for add entry or check existing data for a user. 
# When adding a new entry, there should be an option for searching for an existing user or adding a new user to the database. 

import tkinter as tk

def button_clicked():
    print("Button clicked!")

root = tk.Tk()

# Creating a button with specified options
button = tk.Button(root, 
                   text="Click Me", 
                   command=button_clicked,
                   activebackground="blue", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgray",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=10,
                   pady=5,
                   width=15,
                   wraplength=100)

button.pack(padx=20, pady=20)

root.mainloop()