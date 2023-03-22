# =====Importing libraries=====

from datetime import datetime

# =====Classes=====


class colour:
    """Class for formatting text
    Taken from https://stackoverflow.com/questions/8924173/how-can-i-print-bold-text-in-python"""

    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ====Functions====


def read_users():
    """ Reads users.txt, obtains available users and adds each user to dictionary
    Returns dictionary of available users"""

    # initialise empty dictionary for users
    user_info = dict()

    # reads user.txt for usernames and passwords
    with open("user.txt", "r", encoding="utf-8") as user_file:
        users = user_file.readlines()
        # loop through each user and update dict
        for user in users:
            user = user.strip()
            user = user.split(", ")
            # adds each username and password to dict
            user_info.update({user[0]: user[1]})

    return user_info


def write_users(user_info):
    """ Writes current users to file. Takes dictionary of users as argument"""

    with open("user.txt", "w", encoding="utf-8") as user_file:
        # loop through all items of dict and updates file
        # ensure no empty line at beginning of file
        first_line = ""
        for username, password in user_info.items():
            user = f"{first_line}{username}, {password}"
            user_file.write(user)
            first_line = "\n"


def read_tasks():
    """ Reads tasks from file and stores in list
    Returns the list"""

    with open("tasks.txt", "r", encoding="utf-8") as tasks_file:
        tasks = tasks_file.readlines()
    tasks = [task.strip() for task in tasks]  # strips new line at end

    return tasks


def write_tasks(tasks):
    "Writes the list current tasks to file. Takes list of tasks as argument"

    with open("tasks.txt", "w", encoding="utf-8") as tasks_file:
        # ensure no empty line at beginning of file
        first_line = ""
        for task in tasks:
            tasks_file.write(f"{first_line}{task}")
            first_line = "\n"


def log_on(user_info):
    """Log in a user into the system. Takes dictionary of users as arguments
    Returns logged in user and password"""

    while True:
        # asks for new user
        current_user = input(f"{colour.BOLD}Username: ")
        # checks for valid username
        if current_user not in user_info:
            print(f"{current_user} does not exist. Please enter a valid username.\n")
            continue
        else:
            # checks the password for user
            password = input(f"{colour.BOLD}Password: ")
            if password != user_info[current_user]:
                print("Incorrect password\n")
                continue
            else:
                break

    print(f"\nLogged in successfully as {current_user}{colour.END}\n")

    return current_user


def show_menu(current_user):
    """Presents the menu to the user. Different menu for admin
    Returns the selected function"""

    # presenting the menu to the user and
    if current_user == "admin":
        menu = input(f'''{colour.BOLD}{colour.YELLOW}Select one of the following options below:{colour.END}
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
s - Display statistics
e - Exit
''').lower()
    else:
        menu = input(f'''{colour.BOLD}{colour.YELLOW}Select one of the following options below:{colour.END}
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
''').lower()

    return menu


def reg_user():
    """Registers a user into the system. Only if current user is admin can this function be accessed."""

    print("\nRegistering User\n")
    new_username = input("Please enter new user's username: ")

    # checks if user already exists, if not, adds user to user_info of usernames
    while new_username in user_info:
        print(
            f"\n{new_username} is already registered. Try again.\n")
        new_username = input("Please enter new user's username: ")

    # sets password for new user
    new_password = input("Please enter new user's password: ")
    confirm_pass = input("Please re-enter the password: ")

    # checks if password matches both times and writes to file if match
    while new_password != confirm_pass:
        print("\nPasswords do not match, try again\n")
        new_password = input("Please enter new user's password: ")
        confirm_pass = input("Please re-enter the password: ")

    print("\nPasswords match, user successfully registered\n")

    # update dictionary
    user_info.update({new_username: new_password})


def add_task():
    """Assigns and adds a task for a user in the system"""

    # gets today's date
    today = datetime.today()

    print("\nAdding Task\n")

    # gets task details from user
    assign_to = input("Please enter the user to assign the task to: ")
    # check is user exists
    while assign_to not in user_info:
        print(f"\n{assign_to} is not a valid user\n")
        assign_to = input("Please enter the user to assign the task to: ")

    title = input("Please enter the title of the task: ")
    description = input("Please enter the description of the task: ")
    assign_date = today.strftime("%d %b %Y")

    due_date_str = input("Please enter the due date of the task: ")
    due_date = datetime.strptime(due_date_str, "%d %b %Y")
    # checks if the due date is after the assign date
    while due_date.date() < today.date():
        print(f"\nPlease enter a date in the future\n")
        due_date_str = input("Please enter the due date of the task: ")
        due_date = datetime.strptime(due_date_str, "%d %b %Y")

    # adds task to task list
    tasks.append(
        f"{assign_to}, {title}, {description}, {assign_date}, {due_date}, No")

    print("\nTask successfully added and assigned\n")


def view_all():
    """Views all tasks available in the system"""

    print(f"{colour.BOLD}{colour.RED}All Tasks{colour.END}")
    # split task sections and loop through all tasks
    for counter, task in enumerate(tasks, start=1):
        sections = task.split(", ")
        # display task list
        print(f"""
________________________________________________________________________________
{colour.BOLD}{colour.RED}Task {counter}{colour.END}
Task:                                                          {sections[1]}
Assigned to:                                                   {sections[0]}
Date assigned:                                                 {sections[3]}
Due date:                                                      {sections[4]}
Task Complete?                                                 {sections[5]}
Task description:
    {sections[2]}
________________________________________________________________________________
""")


def view_mine(current_user):
    """Displays all tasks that are available for the current user.
    Allows some editing of the tasks"""

    print(f"{colour.BOLD}{colour.RED}My Tasks{colour.END}")

    while True:
        # counter for number of tasks the current user has
        counter = 0
        # initialise empty list to store indices of current user's tasks
        user_tasks = list()

        # split task sections
        for index, task in enumerate(tasks, start=1):
            sections = task.split(", ")
            # display task list after checking who is logged in
            if sections[0] == current_user:
                counter += 1
                user_tasks.append(index)
                # adds current user's tasks to new list
                print(f"""
    ________________________________________________________________________________
    {colour.BOLD}{colour.RED}Task: {index}{colour.END}
    Task:                                                          {
        sections[1]}
    Assigned to:                                                   {sections[0]}
    Date assigned:                                                 {sections[3]}
    Due date:                                                      {sections[4]}
    Task Complete?                                                 {sections[5]}
    Task description:
        {sections[2]}
    ________________________________________________________________________________
    """)

        # checks is current user has assigned tasks
        if counter == 0:
            print("You have no tasks!")
            return

        # allows user to select a task or return to menu
        selection = int(input(
            f"{colour.BOLD}{colour.RED}Select a task or enter \"-1\" to return to menu:{colour.END}"))

        if selection == -1:
            print("Returning to menu...")
            return
        # can only edit current user's tasks
        elif selection in user_tasks:
            # selects a task and shows new menu to edit task
            task = tasks[selection-1]
            menu = input(f"""{colour.BOLD}{colour.YELLOW}Select one of the following options below:{colour.END}
m - Mark the task as complete
e - Edit the task
""").lower()

            sections = task.split(", ")
            # mark task as complete and update task
            if menu == "m":
                sections[5] = "Yes"
                task = ", ".join(sections)
                tasks[selection-1] = task
                print(f"Task {selection} marked as complete")
            # Only allow editing if the task is not yet complete
            elif menu == "e" and sections[5] == "Yes":
                print("This task is completed")
            elif menu == "e" and sections[5] == "No":
                print("Editing Task")
                menu = input(f"""{colour.BOLD}{colour.YELLOW}Select one of the following options below:{colour.END}
u - Reassign the task to another user
d - Change the due date of the task
""").lower()
                # reassign the task to a different user and saves the new task
                if menu == "u":
                    new_user = input(
                        "Please enter a user to reassign this task to: ")
                    # ensure user is set up in system
                    while new_user not in user_info:
                        new_user = input(
                            "This user does not exist. Please enter a valid user: ")
                    sections[0] = new_user
                    task = ", ".join(sections)
                    tasks[selection-1] = task
                    print(f"Task reassigned to {new_user}")

                # change the due date of the task
                elif menu == "d":
                    today = datetime.today()
                    new_date = input(
                        "Please enter a new due date: ")
                    new_date_obj = datetime.strptime(new_date, "%d %b %Y")
                    # ensure due date is in future
                    while new_date_obj.date() < today.date():
                        new_date = input(
                            "Please enter a date in the future: ")
                        new_date_obj = datetime.strptime(
                            new_date, "%d %b %Y")
                    sections[4] = new_date
                    task = ", ".join(sections)
                    tasks[selection-1] = task
                    print(f"Due date updated")
                else:
                    print("Not a valid choice,.")
            else:
                print("Not a valid choice.")
        else:
            print("Not a valid task")


def display_statistics():
    """Reads from the generated reports and displays the statistics in the program"""

    # generate reports to read from
    generate_report()

    # displays the task statistics. Already formatted in text file.
    print(f"{colour.BOLD}{colour.RED}Task Statistics{colour.END}")
    with open("task_overview.txt", "r", encoding="utf-8") as task_overview_file:
        lines = task_overview_file.readlines()
        for line in lines:
            line = line.strip()
            print(line)

    # displays the user statistics. Already formatted in text file.
    print(f"\n{colour.BOLD}{colour.RED}User Statistics{colour.END}")
    with open("user_overview.txt", "r", encoding="utf-8") as user_overview_file:
        lines = user_overview_file.readlines()
        for line in lines:
            line = line.strip()
            print(line)


def generate_report():
    """Generates reports for tasks and users. Produces text file for each."""

    # task overview
    today = datetime.today()
    # initialise counters
    completed_tasks = 0
    overdue_tasks = 0
    overdue_incomplete_tasks = 0
    # go through tasks and increment counters as required
    for task in tasks:
        task = task.strip()
        sections = task.split(", ")
        due_date = datetime.strptime(sections[4], "%d %b %Y")
        if sections[5] == "Yes":
            completed_tasks += 1
        if due_date.date() < today.date():
            overdue_tasks += 1
        if sections[5] == "No" and due_date.date() < today.date():
            overdue_incomplete_tasks += 1

    # write and display the report to task overview file
    with open("task_overview.txt", "w", encoding="utf-8") as task_overview:
        task_overview.write(f"Total number of tasks: {len(tasks)}\n")
        task_overview.write(
            f"Total number of completed tasks: {completed_tasks}\n")
        task_overview.write(
            f"Total number of uncompleted tasks: {len(tasks) - completed_tasks}\n")
        task_overview.write(
            f"Total number of incomplete and overdue tasks: {overdue_incomplete_tasks}\n")
        task_overview.write(
            f"Percentage of incomplete tasks: {round((len(tasks) - completed_tasks)/len(tasks) * 100,2)}%\n")
        task_overview.write(
            f"Percentage of overdue tasks: {round(overdue_tasks/len(tasks)*100,2)}%")

    # write and display the report to user overview file
    with open("user_overview.txt", "w", encoding="utf-8") as user_overview:
        user_overview.write(f"Total number of users: {len(user_info)}\n")
        user_overview.write(
            f"Total number of tasks: {len(tasks)}\n\n")

        # information on each user in the system
        for user in user_info.keys():
            task_counter = 0
            completed_counter = 0
            overdue_incomplete_counter = 0

            # tasks status for each user
            for task in tasks:
                task = task.strip()
                sections = task.split(", ")
                if user == sections[0]:
                    task_counter += 1
                    if sections[5] == "Yes":
                        completed_counter += 1
                    due_date = datetime.strptime(sections[4], "%d %b %Y")
                    if sections[5] == "No" and due_date.date() < today.date():
                        overdue_incomplete_counter += 1

            user_overview.write(f"{user}\n")
            user_overview.write(f"Total number of tasks: {task_counter}\n")
            user_overview.write(
                f"Percentage of total tasks: {round(task_counter/len(tasks)*100,2)}%\n")
            user_overview.write(
                f"Percentage of completed tasks: {round(completed_counter/task_counter*100,2)}%\n")
            user_overview.write(
                f"Percentage of incomplete tasks: {round((task_counter-completed_counter)/task_counter*100,2)}%\n")
            user_overview.write(
                f"Percentage of incomplete and overdue tasks: {round(overdue_incomplete_counter/task_counter*100,2)}%\n\n")


# ====Login Section====

print(f"{colour.BOLD}{colour.UNDERLINE}{colour.CYAN}Welcome to the Task Manager. Please login.\n{colour.END}")

# read available users and passwords from input.txt and stores in dictionary
user_info = read_users()
# gets tasks from tasks.txt
tasks = read_tasks()
# logs on and sets current user
current_user = log_on(user_info)

# ====Menu Section====

while True:
    # display menu depending on the current user
    menu = show_menu(current_user)
    # Register new user if current user is admin
    if menu == 'r' and current_user == "admin":
        reg_user()
    # Add new task to tasks file
    elif menu == 'a':
        add_task()
    # Displays all tasks to user
    elif menu == 'va':
        view_all()
    # Only display tasks that have been assigned to logged in user
    elif menu == 'vm':
        view_mine(current_user)
    # display statistics if current user is admin
    elif menu == "s" and current_user == "admin":
        display_statistics()
    elif menu == "gr" and current_user == "admin":
        generate_report()
    # Exits program
    elif menu == 'e':
        # Save updated users and tasks to files
        write_tasks(tasks)
        write_users(user_info)
        print('Goodbye!!!')
        exit()
    else:
        print("\nYou have made a wrong choice, please try again\n")
