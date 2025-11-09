import customtkinter as ctk
from tkinter import messagebox
import Backend

#https://www.geeksforgeeks.org/python/create-a-modern-login-ui-using-customtkinter-module-in-python/


# Selecting GUI theme - dark, light , system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x400")
app.title("Monash University Secured Electronic Health Record")


def login():
    valid_login = Backend.login(user_entry.get(), user_pass.get())
    print("Login Button Pushed")
    if valid_login:
        # This is where we would start destroy the login window and open the data entry windows
        messagebox.showinfo("Valid Login", "Good Login")
    if not valid_login:
        messagebox.showwarning("Invalid Login", "Incorrect Username or Password. Please try again.")
    return
    username = "Geeks"
    password = "12345"
    new_window = ctk.CTkToplevel(app)

    new_window.title("New Window")

    new_window.geometry("350x150")

    if user_entry.get() == username and user_pass.get() == password:
        tkmb.showinfo(title="Login Successful",message="You have logged in Successfully")
        ctk.CTkLabel(new_window,text="GeeksforGeeks is best for learning ANYTHING !!").pack()
    elif user_entry.get() == username and user_pass.get() != password:
        tkmb.showwarning(title='Wrong password',message='Please check your password')
    elif user_entry.get() != username and user_pass.get() == password:
        tkmb.showwarning(title='Wrong username',message='Please check your username')
    else:
        tkmb.showerror(title="Login Failed",message="Invalid Username and password")


frame = ctk.CTkFrame(master=app)
frame.pack(pady=20,padx=40,fill='both',expand=True)

label = ctk.CTkLabel(master=frame,text='User Login')
label.pack(pady=12,padx=10)


user_entry= ctk.CTkEntry(master=frame,placeholder_text="Username")
user_entry.pack(pady=12,padx=10)

user_pass= ctk.CTkEntry(master=frame,placeholder_text="Password",show="*")
user_pass.pack(pady=12,padx=10)


button = ctk.CTkButton(master=frame,text='Login',command=login)
button.pack(pady=12,padx=10)

app.mainloop()