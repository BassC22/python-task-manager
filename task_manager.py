import os
from datetime import datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"

username_password = {}
task_list = []
task_counter = 0

# Function to register a new user
def reg_user():
    while True:
        username = input("Enter a username: ")
        # check to see if username already exists
        if username in username_password:
            print("Username already exists. Please enter a new username.")
        else:
            break
    password = input("Enter a password: ")
    username_password[username] = password
    with open("user.txt", "a") as user_file:
        user_file.write(f"{username}\n")
        user_file.write(f"{password}\n")
    print("User registered successfully.")

# Function to add a new task
def add_task():
    global task_counter
    username = input("Enter your username: ")
    title = input("Enter the task title: ")
    description = input("Enter the task description: ")
    due_date = input("Enter the due date (YYYY-MM-DD): ")
    assigned_date = datetime.now().strftime(DATETIME_STRING_FORMAT)
    
    task_counter += 1
    task = {
        "task_number": task_counter,
        "username": username,
        "title": title,
        "description": description,
        "due_date": due_date,
        "assigned_date": assigned_date,
        "completed": False
    }
    task_list.append(task)
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"{task_counter};{username};{title};{description};{due_date};{assigned_date};No\n")
    print("Task added successfully.")

def check_user_file():
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin\n")
            default_file.write("password\n")

check_user_file()


# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    if user:
        username, password = user.split(';')
        username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Function to view tasks assigned to the current user
def view_mine():
    username = input("Enter your username: ")
    found_tasks = False
    for i, task in enumerate(task_list):
        if task['username'] == username:
            found_tasks = True
            disp_str = f"Task {task['task_number']}:\n"
            disp_str += f"Title: {task['title']}\n"
            disp_str += f"Assigned to: {task['username']}\n"
            disp_str += f"Due Date: {task['due_date']}\n"
            disp_str += f"Task Description:\n{task['description']}\n"
            disp_str += f"Completed: {'Yes' if task['completed'] else 'No'}\n"
            print(disp_str)
    if not found_tasks:
        print("No tasks found for the given username.")

    task_number = input("Enter the task number to edit, or -1 to return to the main menu: ")

    task_number = int(task_number)
    if task_number == -1:
        return True
    
    task_number -= 1
    if task_number < 0 or task_number >= len(task_list):
        print("Invalid task number. Please enter a valid task number.")
        return False
    
    selected_task = task_list[task_number]
    print("Selected Task:")
    print(f"Title: {selected_task['title']}")
    print(f"Assigned to: {selected_task['username']}")
    print(f"Due Date: {selected_task['due_date']}")
    print(f"Task Description: {selected_task['description']}")
    print(f"Completed: {'Yes' if selected_task['completed'] else 'No'}")

    edit_option = input("Select an option: (1) Edit Task, (2) Mark as Complete, (3) Return to Main Menu: ")
    if edit_option == "1":
        edit_task(task_number)
    elif edit_option == "2":
        mark_task_completion(task_number)
    elif edit_option == "3":
        return True
    else:
        print("Invalid option. Returning to the main menu.")
    return False

# Function to edit a task
def edit_task(task_number):
    selected_task = task_list[task_number]
    print("Editing Task:")
    print(f"Title: {selected_task['title']}")
    print(f"Assigned to: {selected_task['username']}")
    print(f"Due Date: {selected_task['due_date']}")
    print(f"Task Description: {selected_task['description']}")

    new_title = input("Enter the new title (or press Enter to keep the current one): ")
    new_description = input("Enter the new description (or press Enter to keep the current one): ")
    new_due_date = input("Enter the new due date (YYYY-MM-DD) (or press Enter to keep the current one): ")

    if new_title:
        selected_task['title'] = new_title
    if new_description:
        selected_task['description'] = new_description
    if new_due_date:
        selected_task['due_date'] = new_due_date

    print("Task updated successfully.")

# Function to mark a task as completed
def mark_task_completion(task_number):
    selected_task = task_list[task_number]
    print("Selected Task:")
    print(f"Title: {selected_task['title']}")
    print(f"Assigned to: {selected_task['username']}")
    print(f"Due Date: {selected_task['due_date']}")
    print(f"Task Description: {selected_task['description']}")
    print(f"Completed: {'Yes' if selected_task['completed'] else 'No'}")

    completion_option = input("Are you sure you want to mark this task as complete? (y/n): ")
    if completion_option.lower() == "y":
        selected_task['completed'] = True
        print("Task marked as completed.")
    else:
        print("Task completion status remains unchanged.")

# Function to view all tasks
def view_all():
    for i, task in enumerate(task_list):
        disp_str = f"Task {i + 1}:\n"
        disp_str += f"Title: {task['title']}\n"
        disp_str += f"Assigned to: {task['username']}\n"
        disp_str += f"Due Date: {task['due_date']}\n"
        disp_str += f"Task Description:\n{task['description']}\n"
        disp_str += f"Completed: {'Yes' if task['completed'] else 'No'}\n"
        print(disp_str)

# Function for overdue/incomplete tasks

def get_num_overdue_tasks():
    num_overdue = 0
    current_date = datetime.now().date()
    for task in task_list:
        due_date = datetime.strptime(task['due_date'], DATETIME_STRING_FORMAT).date()
        if not task['completed'] and due_date < current_date:
            num_overdue += 1
    return num_overdue

def get_percentage_incomplete():
    num_tasks = len(task_list)
    num_completed = sum(task['completed'] for task in task_list)
    return (num_tasks - num_completed) / num_tasks * 100

def get_percentage_overdue():
    num_overdue = get_num_overdue_tasks()
    num_tasks = len(task_list)
    return num_overdue / num_tasks * 100

# Function to generate reports
def generate_reports():
    num_users = len(username_password)
    num_tasks = len(task_list)
    num_completed = sum(task['completed'] for task in task_list)

    with open("task_overview.txt", "w") as task_report_file:
        task_report_file.write("Task Overview Report\n\n")
        task_report_file.write(f"Total number of tasks: {num_tasks}\n")
        task_report_file.write(f"Total number of completed tasks: {num_completed}\n")
        task_report_file.write(f"Total number of uncompleted tasks: {num_tasks - num_completed}\n")
        task_report_file.write(f"Total number of tasks that are overdue: {get_num_overdue_tasks()}\n")
        task_report_file.write(f"Percentage of tasks that are incomplete: {get_percentage_incomplete():.2f}%\n")
        task_report_file.write(f"Percentage of tasks that are overdue: {get_percentage_overdue():.2f}%\n")

    with open("user_overview.txt", "w") as user_report_file:
        user_report_file.write("User Overview Report\n\n")
        user_report_file.write(f"Total number of users: {num_users}\n")
        user_report_file.write(f"Total number of tasks generated and tracked: {num_tasks}\n\n")

        for username, password in username_password.items():
            user_tasks = [task for task in task_list if task['username'] == username]
            num_user_tasks = len(user_tasks)
            user_completed_tasks = sum(task['completed'] for task in user_tasks)
            user_incomplete_tasks = num_user_tasks - user_completed_tasks
            user_overdue_tasks = sum(task['due_date'] < datetime.now().date() and not task['completed'] for task in user_tasks)

            user_report_file.write(f"Username: {username}\n")
            user_report_file.write(f"Password: {password}\n")
            user_report_file.write(f"Total number of tasks assigned to user: {num_user_tasks}\n")
            user_report_file.write(f"Percentage of total tasks assigned to user: {num_user_tasks / num_tasks * 100:.2f}%\n")
            user_report_file.write(f"Percentage of tasks assigned to user that are completed: {user_completed_tasks / num_user_tasks * 100:.2f}%\n")
            user_report_file.write(f"Percentage of tasks assigned to user that must still be completed: {user_incomplete_tasks / num_user_tasks * 100:.2f}%\n")
            user_report_file.write(f"Percentage of tasks assigned to user that are overdue: {user_overdue_tasks / num_user_tasks * 100:.2f}%\n\n")

    print("Task and user overview reports generated successfully.")

# Function to display statistics
def display_statistics():
    if not os.path.exists("tasks.txt"):
        print("No tasks found. Please add tasks first.")
        return
    num_tasks = 0
    num_completed = 0
    num_incomplete = 0
    num_overdue = 0

    with open("tasks.txt", "r") as task_file:
        for line in task_file:
            attrs = line.strip().split(";")
            completed = attrs[5].lower() == "yes"
            if completed:
                num_completed += 1
            else:
                num_incomplete += 1

            due_date = datetime.strptime(attrs[3], DATETIME_STRING_FORMAT).date()
            if not completed and due_date < datetime.now().date():
                num_overdue += 1

            num_tasks += 1
    
    print("Statistics:")
    print(f"Total tasks: {num_tasks}")
    print(f"Completed tasks: {num_completed}")
    print(f"Incomplete tasks: {num_incomplete}")
    print(f"Overdue tasks: {num_overdue}")

# Load existing tasks from tasks.txt file
if os.path.exists("tasks.txt"):
    with open("tasks.txt", "r") as task_file:
        for line in task_file:
            attrs = line.strip().split(";")
            new_task = {
                "username": attrs[0],
                "title": attrs[1],
                "description": attrs[2],
                "due_date": attrs[3],
                "assigned_date": datetime.strptime(attrs[4], DATETIME_STRING_FORMAT),
                "completed": attrs[5].lower() == "yes"
            }
            task_list.append(new_task)

# Load existing username and password from user.txt file
username_password = {}
if os.path.exists("user.txt"):
    with open("user.txt", "r") as user_file:
        for line in user_file:
            attrs = line.strip().split(";")
            username_password[attrs[0]] = attrs[1]

# Main program loop

while True:
    print("\nMenu:")
    print("r: Register User")
    print("a: Add Task")
    print("vm: View My Tasks")
    print("va: View All Tasks")
    print("gr: Generate Reports")
    print("ds: Display Statistics")
    print("e:. Exit")

    choice = input("Enter your choice: ")

    if choice == "r":
        reg_user()
    elif choice == "a":
        add_task()
    elif choice == "vm":
        view_mine()
    elif choice == "va":
        view_all()
        task_number = input("Enter the task number, or -1 to return to the main menu: ")
        if task_number == "-1":
                continue
        task_number = int(task_number) - 1
        if task_number < 0 or task_number >= len(task_list):
                print("Invalid task number. Please enter a valid task number.")
                task_number = None
                continue
    elif choice == "gr":
        generate_reports()
    elif choice == "ds":
        if curr_user == "admin":
            display_statistics()
        else:
            print("You do not have permission to view statistics.")
        display_statistics()
    elif choice == "e":
        break
    else:
        print("Invalid choice. Please enter a valid option.")

print("Goodbye!")
