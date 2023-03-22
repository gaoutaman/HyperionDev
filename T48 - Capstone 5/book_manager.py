""" Program to be used by book shop clerk. Allows management of books
    - Add new books
    - Update book information
    - Delete books from database
    - Search database for books
"""
############################################
# Libraries and Packages

import sqlite3

############################################
# Functions


def enter_book():
    """Function to enter/add new books into the database"""
    pass


def update_book():
    """Update details of a book in the database"""
    pass


def delete_book():
    """Delete a book from the database"""
    pass


def search_books():
    """Search for books in the database"""
    pass


############################################
# Main

# Initialise the database
# Connect the database
db = sqlite3.connect("ebookstore")
# Get a cursor object
cursor = db.cursor()

# Create a table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT,
                                    author TEXT, quantity INTEGER)
"""
)
print("Connection established to book database...")

# insert rows to table
books = [
    (3001, "A Tale of Two Cities", "Charles Dickens", 30),
    (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
    (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
    (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12),
]

# If database with these unique rows exists, don't try to add them again
try:
    cursor.executemany(
        """ INSERT INTO books(id, title, author, quantity) VALUES(?,?,?,?)""", books
    )
except sqlite3.IntegrityError:
    print("Initial records already exist")

db.commit()
db.close()

# Main menu to navigate through the program.
while True:
    # Book menu
    print("\nWelcome to Book Manager!\n")
    print("Menu")
    print(
        """
1   - Enter book
2   - Update book
3   - Delete book
4   - Search books
0   - Exit
"""
    )
    try:
        menu = int(input("Please select an option: "))
        # menu options
        if menu == 1:
            enter_book()
            pass
        elif menu == 2:
            update_book()
            # connect the database (create new file)
            db = sqlite3.connect("ebookstore")
            # get a cursor object
            cursor = db.cursor()
            # View all records to check
            cursor.execute(""" SELECT * FROM books""")
            students = cursor.fetchall()
            print(students)
            db.close()
        elif menu == 3:
            delete_book()
            pass
        elif menu == "4":
            search_books()
            pass
        elif menu == 0:
            print("Exiting...")
            exit()
        else:
            print("Invalid option")
    except ValueError:
        # ensure correct type is entered
        print("Please enter an integer....")
        continue
