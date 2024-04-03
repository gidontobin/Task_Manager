import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManagerApp
import sqlite3
from hashlib import sha256

# Create a SQLite connection
conn = sqlite3.connect('task_manager.db')
cursor = conn.cursor()

def hash_password(password):
    """Hashes the given password using SHA-256."""
    return sha256(password.encode()).hexdigest()

def load_users():
    """Load users from SQLite database."""
    users = {}
    cursor.execute("SELECT username, password FROM users")
    for row in cursor.fetchall():
        username, password_hash = row
        users[username] = password_hash
    return users

def save_user(username, password):
    """Save user to SQLite database."""
    password_hash = hash_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
    conn.commit()

# Function to handle login button click
def login():
    root.withdraw()
    users = load_users()

    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.configure(background="black")  # Set background color
    login_window.state('zoomed')

    # Entry widget for username
    username_label = tk.Label(login_window, text="Username:", background="black",foreground="white", font=("Arial", 20))
    username_label.place(relx=0.4, rely=0.4, anchor="center")
    username_entry = tk.Entry(login_window, font=("Arial", 20))
    username_entry.place(relx=0.55, rely=0.4, anchor="center")

    # Entry widget for password
    password_label = tk.Label(login_window, text="Password:", background="black",foreground="white", font=("Arial", 20))
    password_label.place(relx=0.4, rely=0.5, anchor="center")
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 20))
    password_entry.place(relx=0.55, rely=0.5, anchor="center")

    # Function to validate login
    def validate_login(event):
        username = username_entry.get()
        if username in users:
            password = password_entry.get()
            if hash_password(password) == users[username]:
                login_window.destroy()
                task_manager_app(username)
            else:
                login_window.destroy()
                messagebox.showerror("Login", "Incorrect Username or password!")
                root.deiconify()
                root.state('zoomed')
        else:
            login_window.destroy()
            messagebox.showerror("Login", "Incorrect Username or password!")
            root.deiconify()
            root.state('zoomed')

    # Button to confirm login
    confirm_button = tk.Button(login_window, text="Login", background="#009688", foreground="white", font=("Arial", 20, "bold"))
    confirm_button.place(relx=0.5, rely=0.6, anchor="center")
    confirm_button.bind('<Button-1>', validate_login)
    login_window.bind('<Return>', validate_login)
    def show_again():
        login_window.destroy()
        root.deiconify()
        root.state('zoomed')
    login_window.protocol("WM_DELETE_WINDOW", show_again)

# Function to handle register button click
def register():
    root.withdraw()
    users = load_users()

    register_window = tk.Tk()
    register_window.title("Register")
    register_window.configure(background="black")  # Set background color
    register_window.state('zoomed')


    # Entry widget for username
    username_label = tk.Label(register_window, text="Username:", background="black",foreground="white", font=("Arial", 20))
    username_label.place(relx=0.4, rely=0.4, anchor="center")
    username_entry = tk.Entry(register_window, font=("Arial", 20))
    username_entry.place(relx=0.55, rely=0.4, anchor="center")

    # Entry widget for password
    password_label = tk.Label(register_window, text="Password:", background="black",foreground="white", font=("Arial", 20))
    password_label.place(relx=0.4, rely=0.5, anchor="center")
    password_entry = tk.Entry(register_window, show="*", font=("Arial", 20))
    password_entry.place(relx=0.55, rely=0.5, anchor="center")

    # Function to validate registration
    def validate_registration(event):
        username = username_entry.get()
        if username:
            if username in users:
                messagebox.showerror("Register", "Username already exists!")
            else:
                password = password_entry.get()
                if password:
                    save_user(username, password)
                    messagebox.showinfo("Register", "Registration successful!")
                    register_window.destroy()
                    root.deiconify()
                    root.state('zoomed')
                else:
                    messagebox.showerror("Register", "Password cannot be empty!")
                    register_window.destroy()
                    root.deiconify()
                    root.state('zoomed')
        else:
            messagebox.showerror("Register", "Username cannot be empty!")
            register_window.destroy()
            root.deiconify()
            root.state('zoomed')

    # Button to confirm registration
    confirm_button = tk.Button(register_window, text="Register", background="#009688", foreground="white", font=("Arial", 20, "bold"))
    confirm_button.place(relx=0.5, rely=0.6, anchor="center")
    confirm_button.bind('<Button-1>', validate_registration)
    register_window.bind('<Return>', validate_registration)
    def show_again():
        register_window.destroy()
        root.deiconify()
        root.state('zoomed')
    register_window.protocol("WM_DELETE_WINDOW", show_again)

# Function to launch the task manager app
def task_manager_app(username):
    root.destroy()  # Destroy the login/registration window
    app = TaskManagerApp(username)  # Launch the task manager app with username and tasks
    app.mainloop()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Create a Tkinter window for login/register
root = tk.Tk()
root.title("Task Manager Login/Register")
root.configure(background="black")  # Set background color


# Entry widget for task description
task_description_label = tk.Label(root, text="Task Manager", background="black",foreground="white", font=("Arial", 30))
task_description_label.place(relx=0.5, rely=0.3, anchor="center")

root.protocol("WM_DELETE_WINDOW", on_closing)

# Set window size to fill the screen
root.state('zoomed')

# Add login and register buttons
login_button = tk.Button(root, text="Login", command=login, background="#009688", foreground="white", font=("Arial", 20, "bold"))
login_button.place(relx=0.4, rely=0.5, anchor="center")

register_button = tk.Button(root, text="Register", command=register, background="#009688", foreground="white", font=("Arial", 20, "bold"))
register_button.place(relx=0.6, rely=0.5, anchor="center")

root.mainloop()
