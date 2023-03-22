# =====Importing libraries===========

from datetime import date

# ====Login Section====

# initialise empty lists
usernames = list()
passwords = list()

# gets today's date
today = date.today()

# reads users.txt, obtains available users, separates usernames and passwords
with open("user.txt", "r", encoding="utf-8") as user_file:
    users = user_file.readlines()
    for user in users:
        user = user.strip()
        user = user.split(", ")
        usernames.append(user[0])
        passwords.append(user[1])

# logging in
while True:
    username = input("Username: ")
    # checks for valid username
    if username not in usernames:
        print("Please enter a valid username\n")
        continue
    else:
        # gets index of user to ensure corresponding password is checked
        user_index = usernames.index(username)
        password = input("Password: ")
        if password != passwords[user_index]:
            print("Incorrect password\n")
            continue
        else:
            break

print(f"\nLogged in successfully as {username}\n")


while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.

    if username == "admin":
        menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
s - Display statistics
e - Exit
: ''').lower()
    else:
        menu = input('''Select one of the following options below:
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    # Register new user if current user is admin
    if menu == 'r' and username == "admin":

        print("\nRegistering User\n")
        new_username = input("Please enter new user's username: ")

        # checks if user already exists
        if new_username in usernames:
            print(f"\n{new_username} is already registered\n")
            continue
        else:
            usernames.append(new_username)

        new_password = input("Please enter new user's password: ")
        confirm_pass = input("Please re-enter the password: ")

        # checks if password matches both times and writes to file if match
        if new_password == confirm_pass:
            new_user = (f"\n{new_username}, {new_password}")
            passwords.append(new_password)
            # writes new user to users.txt
            with open("user.txt", "a", encoding="utf-8") as user_file:
                user_file.write(new_user)
                print("\nPasswords match, user successfully registered\n")
        else:
            print("\nPasswords do not match, returning to menu\n")

    # Add new task to tasks file
    elif menu == 'a':

        print("\nAdding Task\n")

        # gets task details from user
        assign_to = input("Please enter the user to assign the task to: ")
        # check is user exists
        if assign_to not in usernames:
            print(f"\n{assign_to} is not a valid user\n")
            continue

        title = input("Pleas enter the title of the task: ")
        description = input("Please enter the description of the task: ")
        assign_date = today.strftime("%d %b %Y")

        due_date = input("Please enter the due date of the task: ")
        # checks if the due date is after the assign date
        if due_date < assign_date:
            print(f"\nPlease enter a date in the future\n")
            continue

        # writes to file
        with open("tasks.txt", "a", encoding="utf-8") as tasks_file:
            tasks_file.write(
                f"\n{assign_to}, {title}, {description}, {assign_date}, {due_date}, No")
        print("\nTask successfully added and assigned\n")

    # Displays all tasks to user
    elif menu == 'va':

        with open("tasks.txt", "r", encoding="utf-8") as tasks_file:
            lines = tasks_file.readlines()
            # split task sections
            for line in lines:
                line = line.strip()
                sections = line.split(", ")
                # display task list
                print(f"""
________________________________________________________________________________

Task:                                                          {sections[1]} 
Assigned to:                                                   {sections[0]}
Date assigned:                                                 {sections[3]}
Due date:                                                      {sections[4]}
Task Complete?                                                 {sections[5]}
Task description: 
    {sections[2]}
________________________________________________________________________________
""")

    # Only display tasks that have been assigned to logged in user
    elif menu == 'vm':

        with open("tasks.txt", "r", encoding="utf-8") as tasks_file:
            lines = tasks_file.readlines()
            # split task sections
            for line in lines:
                line = line.strip()
                sections = line.split(", ")
                # display task list after checking who is logged in
                if sections[0] == username:
                    print(f"""
________________________________________________________________________________

Task:                                                          {sections[1]} 
Assigned to:                                                   {sections[0]}
Date assigned:                                                 {sections[3]}
Due date:                                                      {sections[4]}
Task Complete?                                                 {sections[5]}
Task description: 
    {sections[2]}
________________________________________________________________________________
""")

    # display statistics if current user is admin
    elif menu == "s" and username == "admin":

        # gets total number of users
        with open("user.txt", "r") as user_file:
            lines = user_file.readlines()
            total_users = len(lines)

        # gets total number of tasks
        with open("tasks.txt", "r") as task_file:
            lines = task_file.readlines()
            total_tasks = len(lines)

        # displays statistics
        print(f"""
________________________________________________________________________________

Total number of tasks: {total_tasks}

Total number of users: {total_users}
________________________________________________________________________________
""")

    # Exits program
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("\nYou have made a wrong choice, please try again\n")
