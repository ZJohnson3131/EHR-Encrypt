import tkinter as tk
from tkinter import ttk, messagebox


class LoginWindow:
    """Initial Login Window"""
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x250")

        tk.Label(root, text="Username:", font=('Arial', 12)).pack(pady=10)
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack()

        tk.Label(root, text="Password:", font=('Arial', 12)).pack(pady=10)
        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.pack()

        tk.Button(root, text="Login", width=12, bg="#4CAF50", fg="white",
                  command=self.login).pack(pady=20)

    def login(self):
        # For now: passive login (no validation)
        self.root.destroy()
        open_main_app()


class SearchTab:
    """Search Functionality Tab"""
    def __init__(self, parent):
        tk.Label(parent, text="Search Value:", font=('Arial', 11)).pack(pady=5)
        self.search_entry = tk.Entry(parent, width=40)
        self.search_entry.pack()

        tk.Button(parent, text="Search", bg="#4CAF50", fg="white",
                  command=self.search).pack(pady=10)

        # Search results table
        self.tree = ttk.Treeview(parent, columns=("ID", "Name", "Gender", "City", "Country"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("City", text="City")
        self.tree.heading("Country", text="Country")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Example data
        data = [
            (1, "Alex", "Male", "GGN", "India"),
            (2, "Dinesh Rana", "Male", "New Delhi", "India"),
            (3, "Mrs. Sinha", "Female", "Pune", "India"),
        ]
        for row in data:
            self.tree.insert("", tk.END, values=row)

    def search(self):
        val = self.search_entry.get()
        if val:
            messagebox.showinfo("Search", f"Searched for: {val}")
        else:
            messagebox.showwarning("Input Required", "Please enter a search value")


class DataEntryTab:
    """Data Entry Form Tab"""
    def __init__(self, parent):
        form_fields = [
            ("Name", ""), ("Gender", ""), ("Qualification", ""), ("City", ""), ("State", ""), ("Country", "")
        ]

        self.entries = {}
        for i, (label, _) in enumerate(form_fields):
            tk.Label(parent, text=label, font=('Arial', 11)).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            if label == "Gender":
                self.gender_var = tk.StringVar()
                tk.Radiobutton(parent, text="Male", variable=self.gender_var, value="Male").grid(row=i, column=1, sticky='w')
                tk.Radiobutton(parent, text="Female", variable=self.gender_var, value="Female").grid(row=i, column=2, sticky='w')
            else:
                entry = tk.Entry(parent, width=30)
                entry.grid(row=i, column=1, columnspan=2, pady=5)
                self.entries[label] = entry

        tk.Button(parent, text="Submit", width=15, bg="#4CAF50", fg="white", command=self.submit).grid(
            row=len(form_fields)+1, column=1, pady=20)

    def submit(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        data["Gender"] = self.gender_var.get()
        messagebox.showinfo("Submitted Data", f"Data Submitted:\n{data}")


class MainApp:
    """Main Application Window with Tabs and Menu"""
    def __init__(self, root):
        self.root = root
        self.root.title("Data Management Application")
        self.root.geometry("800x500")

        # Menu bar
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Log Out", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menubar)

        # Tabs (Notebook)
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        # Create tabs
        search_frame = ttk.Frame(notebook)
        data_entry_frame = ttk.Frame(notebook)

        notebook.add(search_frame, text="Search")
        notebook.add(data_entry_frame, text="Data Entry")

        # Populate tabs
        SearchTab(search_frame)
        DataEntryTab(data_entry_frame)

    def logout(self):
        self.root.destroy()
        open_login()


# ---------- Window Switching Functions ----------
def open_login():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


def open_main_app():
    root = tk.Tk()
    MainApp(root)
    root.mainloop()


# ---------- Run App ----------
if __name__ == "__main__":
    open_login()
