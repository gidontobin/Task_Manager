**Task Manager Application**

**Overview:**

The Task Manager Application is a Python-based task management system designed to help users organize their tasks efficiently. It provides features for user authentication (login and registration) and allows users to add, delete, edit, and organize tasks by due date.

**Features:**

1. **User Authentication:**
   - Users can register for a new account with a unique username and password.
   - Existing users can log in using their credentials.

2. **Task Management:**
   - Users can add tasks with descriptions, due dates, and completion status.
   - Tasks can be deleted individually.
   - Task details can be edited, including the description, due date, and completion status.
   - Tasks can be organized by due date, allowing users to view tasks in chronological order.

3. **Data Storage:**
   - User credentials and task information are stored in a SQLite database (`task_manager.db`).
   - Task information is also stored locally in JSON format.

**File Structure:**

- `main.py`: Contains the main script responsible for creating the user interface, handling user authentication, and launching the Task Manager application.
- `task_manager.py`: Defines the `TaskManagerApp` class, which implements the Task Manager application interface and functionality.
- `task_manager.db`: SQLite database file for storing user credentials and task information.
- `README.md`: This file provides an overview of the Task Manager application, its features, and file structure.

**Dependencies:**

- Python 3.x
- Tkinter (Python GUI toolkit)
- SQLite3 (Python SQLite interface)
- JSON (JavaScript Object Notation)

**Usage:**

1. Ensure you have Python installed on your system.
2. Install any necessary dependencies using `pip` if not already installed (`pip install tkinter`).
3. Run `main.py` to launch the Task Manager application.
4. Use the login/register interface to authenticate or register as a new user.
5. Once logged in, use the Task Manager interface to add, delete, edit, and organize tasks.

**Contributors:**

- Gidon Tobin
- gidontobin@gmail.com
- https://github.com/gidontobin

**Support:**

For any issues or inquiries, please contact gidontobin@gmail.com. Contributions and feedback are welcome!
