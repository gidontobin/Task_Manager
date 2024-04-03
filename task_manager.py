import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import *
from tkinter import ttk
import json
from datetime import datetime
import sqlite3


class TaskManagerApp(tk.Tk):
    
    alive = False
    #username = ""
    #tasks = []
    
    def load_tasks_from_db(self):
        """Load tasks from the SQLite database."""
        self.cursor.execute("SELECT description, due_date, completed FROM tasks WHERE user_id = ?", (self.username,))
        rows = self.cursor.fetchall()
        for row in rows:
            description, due_date, completed = row
            self.tasks.append({"description": description, "due_date": due_date, "completed": completed})

    def save_tasks_to_db(self):
        # Delete existing tasks for the current user
        self.cursor.execute("DELETE FROM tasks WHERE user_id = ?", (self.username,))
        """Save tasks to the SQLite database."""
        for task in self.tasks:
            description = task["description"]
            due_date = task["due_date"]
            completed = task["completed"]
            self.cursor.execute("INSERT INTO tasks (user_id, description, due_date, completed) VALUES (?, ?, ?, ?)",
                                (self.username, description, due_date, completed))
        self.conn.commit()

    
    
    def load_tasks(self):
        """Load tasks from file."""
        try:
            with open("tasks"+self.username+".json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
    
    def save_tasks(self):
        """Save tasks to file."""
        with open("tasks"+self.username+".json", "w") as file:
            json.dump(self.tasks, file, indent=4)

    def __init__(self, username):
        super().__init__()
        self.title("Task Manager")
        self.configure(background="black")
        self.username = username
        self.tasks = []
        self.conn = sqlite3.connect('task_manager.db')
        self.cursor = self.conn.cursor()
        self.load_tasks_from_db()
        self.state('zoomed')
        
        task_description_label = tk.Label(self, text=username+"'s Task List", background="black",foreground="white", font=("Arial", 30))
        task_description_label.place(relx=0.5, rely=0.1, anchor="center")
        
        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", font=("Arial", 20, "bold"))
        style.configure("Custom.Treeview", font=("Arial", 20))
        style.configure("Custom.Treeview", rowheight=40)  # Adjust the row height here


        self.task_tree = ttk.Treeview(self, columns=("Description", "Due Date", "Completed"), show="headings", selectmode="browse", style="Custom.Treeview")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Due Date", text="Due Date")
        self.task_tree.heading("Completed", text="Completed")
        self.task_tree.place(relx=0.5, rely=0.45, anchor="center")

        self.load_tasks_into_tree()

        self.add_task_button = tk.Button(self, text="Add Task", command=self.show_task_popup, background="#009688", foreground="white", font=("Arial", 20, "bold"))
        self.add_task_button.place(relx=0.4, rely=0.83, anchor="center")
        self.delete_task_button = tk.Button(self, text="Delete Task", command=self.delete_task, background="#009688", foreground="white", font=("Arial", 20, "bold"))
        self.delete_task_button.place(relx=0.6, rely=0.83, anchor="center")
        self.organize_button = tk.Button(self, text="Organize by Due Date", command=self.organize_by_due_date, background="#009688", foreground="white", font=("Arial", 20, "bold"))
        self.organize_button.place(relx=0.5, rely=0.91, anchor="center")

        self.task_tree.bind("<Double-1>", self.edit_task)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
        
    def load_tasks_into_tree(self):
        """Load tasks into the Treeview."""
        for task in self.tasks:
            self.task_tree.insert("", "end", values=(task["description"], task["due_date"], "Yes" if task["completed"] else "No"))
    
    def organize_by_due_date(self):
        if self.alive:
            return
        """Organize tasks by due date."""
        self.tasks.sort(key=lambda x: datetime.strptime(x["due_date"], "%d/%m/%Y"))
        self.task_tree.delete(*self.task_tree.get_children())
        self.load_tasks_into_tree()
    
    def show_task_popup(self):
        if self.alive:
            return
        self.alive = True
        """Show popup window for adding a task."""
        self.popup = tk.Toplevel()
        self.popup.title("Add Task")
        self.popup.configure(background="black")  # Set background color
        self.popup.protocol("WM_DELETE_WINDOW", self.disable_event_pop)

        task_description_label = tk.Label(self.popup, text="Task Description:", background="black",foreground="white", font=("Arial", 20))
        task_description_label.grid(row=0, column=0)
        self.task_description_var = tk.StringVar()
        self.task_description_entry = tk.Entry(self.popup, textvariable=self.task_description_var, font=("Arial", 20))
        self.task_description_entry.grid(row=0, column=1)

        task_due_date_label = tk.Label(self.popup, text="Due Date (DD/MM/YYYY):", background="black",foreground="white", font=("Arial", 20))
        task_due_date_label.grid(row=1, column=0)
        self.task_due_date_var = tk.StringVar()
        self.task_due_date_entry = tk.Entry(self.popup, textvariable=self.task_due_date_var, font=("Arial", 20))
        self.task_due_date_entry.grid(row=1, column=1)

        task_status_label = tk.Label(self.popup, text="Task Status:", background="black",foreground="white", font=("Arial", 20))
        task_status_label.grid(row=2, column=0)
        self.task_status_var = tk.StringVar()
        self.task_status_var.set("Incomplete")  # Set default value
        self.task_status_menu = tk.OptionMenu(self.popup, self.task_status_var, "Incomplete", "Completed")
        self.task_status_menu.config(font=("Arial", 20))
        self.task_status_menu.grid(row=2, column=1)

        confirm_button = tk.Button(self.popup, text="Confirm", command=self.add_task, background="#009688", foreground="white", font=("Arial", 20, "bold"))
        confirm_button.grid(row=3, column=0, columnspan=2)
        
    def add_task(self):
        """Add a new task."""
        task_description = self.task_description_var.get()
        task_due_date = self.task_due_date_var.get()
        task_status = self.task_status_var.get()
        try:
            datetime.strptime(task_due_date, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Please enter the due date in the format DD/MM/YYYY.")
            self.popup.destroy()  # Close the add task popup window
            self.alive = False
            return
        if task_description.strip() != "":  # Check if description is not blank 
            for task in self.tasks:
                if task["description"] == task_description:
                    messagebox.showerror("Error", "Task already exists!")
                    self.popup.destroy()  # Close the add task popup window
                    self.alive = False
                    return
            self.tasks.append({"description": task_description, "due_date": task_due_date, "completed": (task_status == "Completed")})
            self.task_tree.delete(*self.task_tree.get_children())
            self.load_tasks_into_tree()
            self.save_tasks_to_db()  # Save tasks after adding a new task
            self.task_description_entry.delete(0, tk.END)  # Clear task description entry
            self.task_description_var.set("")  # Clear task description variable
            self.task_due_date_entry.delete(0, tk.END)  # Clear due date entry
            self.task_due_date_var.set("")  # Clear due date variable
            self.task_status_var.set("Incomplete")  # Reset task status variable
            self.popup.destroy()  # Close the add task popup window
            self.alive = False
            
            
    def delete_task(self):
        if self.alive:
            return
        """Delete a task."""
        selected_item = self.task_tree.selection()
        if selected_item:
            item = self.task_tree.item(selected_item)
            description = item["values"][0]
            for task in self.tasks:
                if str(task["description"]) == str(description):
                    self.tasks.remove(task)
                    break
            self.task_tree.delete(selected_item)
            self.save_tasks_to_db()

    def disable_event_pop(self):
        self.alive = False
        self.popup.destroy()
    def disable_event_edit(self):
        self.alive = False
        self.edit_popup.destroy()
    
    def edit_task(self, event):
        """Edit a task."""
        selected_item = self.task_tree.selection()
        item1 = self.task_tree.item(selected_item)
        if selected_item:
            if self.alive:
                return
            self.alive = True
            item = self.task_tree.item(selected_item)
            self.edit_popup = tk.Toplevel()
            self.edit_popup.title("Edit Task")
            self.edit_popup.configure(background="black")  # Set background color

            self.edit_popup.protocol("WM_DELETE_WINDOW", self.disable_event_edit)

            task_description_label = tk.Label(self.edit_popup, text="Task Description:", background="black",foreground="white", font=("Arial", 20))
            task_description_label.grid(row=0, column=0)
            self.edit_task_description_var = tk.StringVar(value=item["values"][0])
            self.edit_task_description_entry = tk.Entry(self.edit_popup, textvariable=self.edit_task_description_var, font=("Arial", 20))
            self.edit_task_description_entry.grid(row=0, column=1)

            task_due_date_label = tk.Label(self.edit_popup, text="Due Date (YYYY-MM-DD):", background="black",foreground="white", font=("Arial", 20))
            task_due_date_label.grid(row=1, column=0)
            self.edit_task_due_date_var = tk.StringVar(value=item["values"][1])
            self.edit_task_due_date_entry = tk.Entry(self.edit_popup, textvariable=self.edit_task_due_date_var, font=("Arial", 20))
            self.edit_task_due_date_entry.grid(row=1, column=1)

            task_status_label = tk.Label(self.edit_popup, text="Task Status:", background="black",foreground="white", font=("Arial", 20))
            task_status_label.grid(row=2, column=0)
            self.edit_task_status_var = tk.StringVar(value="Completed" if item["values"][2] else "Incomplete")
            self.edit_task_status_menu = tk.OptionMenu(self.edit_popup, self.edit_task_status_var, "Incomplete", "Completed")
            self.edit_task_status_menu.config(font=("Arial", 20))
            self.edit_task_status_menu.grid(row=2, column=1)

            save_button = tk.Button(self.edit_popup, text="Save", command=self.save_edited_task, background="#009688", foreground="white", font=("Arial", 20, "bold"))
            save_button.grid(row=3, column=1)
            

    def enable_editing(self):
        """Enable editing of task details."""
        self.edit_task_description_entry.config(state=tk.NORMAL)
        self.edit_task_due_date_entry.config(state=tk.NORMAL)
        self.edit_task_status_menu.config(state=tk.NORMAL)

    def save_edited_task(self):
        """Save edited task."""
        selected_item = self.task_tree.selection()
        if selected_item:
            item = self.task_tree.item(selected_item)
            description = item["values"][0]
            for task in self.tasks:
                if task["description"] == description:
                    task_description = self.edit_task_description_var.get()
                    task_due_date = self.edit_task_due_date_var.get()
                    task_completed = True if self.edit_task_status_var.get() == "Completed" else False
                    try:
                        datetime.strptime(task_due_date, "%d/%m/%Y")
                    except ValueError:
                        messagebox.showerror("Error", "Please enter the due date in the format DD/MM/YYYY.")
                        self.edit_popup.destroy()  # Close the add task popup window
                        self.alive = False
                        return
                    if task_description.strip() == "":
                        messagebox.showerror("Error", "No name of task")
                        self.edit_popup.destroy()  # Close the add task popup window
                        self.alive = False
                        return

                    for t in self.tasks:
                        if t["description"] == task_description:
                            if t != task:
                                messagebox.showerror("Error", "Task already exists!")
                                self.edit_popup.destroy()  # Close the add task popup window
                                self.alive = False
                                return
                    task["description"] = task_description
                    task["due_date"] = task_due_date
                    task["completed"] = task_completed
                    break
            # Reload tasks into Treeview
            self.task_tree.delete(*self.task_tree.get_children())
            self.load_tasks_into_tree()
            # Save tasks to file
            self.save_tasks_to_db()
            # Close the edit popup window
            self.edit_popup.destroy()
            self.alive = False

