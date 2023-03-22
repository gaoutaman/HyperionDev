
# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        """
        Constructor - initialise objects with the following properties
        """
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        """
        Returns the cost of the shoes
        """
        return float(self.cost)

    def get_quantity(self):
        """
        Return the quantity of the shoes.
        """
        return int(self.quantity)

    def __str__(self):
        """
        String representation of the class
        """
        return f"{self.product} stock details - Country: {self.country}, Code: {self.code}, Cost: {self.cost}, Quantity: {self.quantity}"


# =============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []
# ==========Functions outside the class==============


def read_shoes_data():
    """
    Read shoes data from inventory.txt and create an instance of the Shoe class. Append the object to list of shoes
    """
    try:
        with open("inventory.txt", "r", encoding="utf-8") as inventory_file:
            lines = inventory_file.readlines()
            # remove first line
            del lines[0]
            # extract information from lines and add to shoe list
            for line in lines:
                line = line.strip()
                sections = line.split(",")
                shoe_list.append(Shoe(sections[0], sections[1],
                                      sections[2], sections[3],  sections[4]))
    except FileNotFoundError:
        # handle error if the inventory file is not found. Exit smoothly
        print("Inventory file not found. Creating empty inventory list file and exiting...")
        with open("inventory.txt", "w", encoding="utf-8") as inventory_file:
            inventory_file.write("Country,Code,Product,Cost,Quantity")
        exit()
    except IndexError:
        # can't delete the header line as file is empty.
        print("File is empty. Creating empty inventory list file and exiting...")
        with open("inventory.txt", "w", encoding="utf-8") as inventory_file:
            inventory_file.write("Country,Code,Product,Cost,Quantity")
        exit()


def capture_shoes():
    '''
    Allows user to capture details about a shoe and add a shoe object to the list
    '''
    # user input
    country = input("Please enter country: ")
    code = input("Please enter code: ")
    product = input("Please enter product: ")
    while True:
        try:
            # ensure numbers are inputted
            cost = float(input("Please enter cost: "))
            quantity = int(input("Please enter quantity: "))
        except ValueError:
            print("Please enter a number...")
            continue
        break
    # add captured shoe to list
    shoe_list.append(Shoe(country, code, product, cost, quantity))

    # add shoe to file. File errors handled in read_shoes_data()
    with open("inventory.txt", "a", encoding='utf8') as inventory_file:
        inventory_file.write(f"\n{country},{code},{product},{cost},{quantity}")


def view_all():
    '''
    View all shoes in stock
    '''
    for shoe in shoe_list:
        print(f"{shoe}\n")


def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    # extract the quantities of all the shoes in the inventory
    amounts = [shoe.get_quantity() for shoe in shoe_list]
    # find out the lowest quantity
    lowest_amount = min(amounts)

    # extract the index of the lowest quantity shoe from shoe list. Ensures multiple lowest quantity shoes are accounted for.
    indices = [i for i in range(len(amounts)) if amounts[i] == lowest_amount]
    restock_shoes = []
    for index in indices:
        restock_shoes.append(shoe_list[index])

    # display shoes with the highest quantity and show as for sale
    print("Running low on supply. The following shoes need to be restocked.\n")
    for i, shoe in enumerate(restock_shoes, start=1):
        print(f"{i}. {shoe}\n")

    # shoe selection on ordering process
    while True:
        try:
            # pick a shoe from available lowest quantity shoes
            selection = int(input("""
Please pick a shoe to restock. Type 0 to exit:
"""))
        except ValueError:
            print("Please enter a number")
            continue

        # exit to menu
        if selection == 0:
            break

        elif selection > 0 and selection <= len(restock_shoes):
            restock_shoe = restock_shoes[selection-1]
            # selects how much of shoe to restock
            while True:
                try:
                    qty = int(input("How much would you like to order?: "))
                except ValueError:
                    print("Please enter a number")
                    continue
                break

            # updates the quantity of the shoe
            print(f"Ordering {qty} shoes...")
            restock_shoe.quantity = restock_shoe.get_quantity() + qty

            # updates shoe list
            for shoe in shoe_list:
                if shoe.code == restock_shoe.code:
                    shoe = restock_shoe

            # update shoe in inventory.txt
            with open("inventory.txt", "w", encoding="utf-8") as inventory_file:
                inventory_file.write(
                    "Country,Code,Product,Cost,Quantity\n")
                # extract information from lines and add to shoe list
                for shoe in shoe_list:
                    if shoe == shoe_list[len(shoe_list)-1]:
                        inventory_file.write(
                            f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")
                    else:
                        inventory_file.write(
                            f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
        else:
            print("Invalid selection.")


def search_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    # initialise list of shoe codes
    shoe_codes = list()

    # get user input to search shoe
    selection = input("Enter shoe code to search: ")
    for shoe in shoe_list:
        shoe_codes.append(shoe.code)
        # prints the selected shoe
        if selection == shoe.code:
            print(shoe)
    # takes care of case when shoe code is not found
    if selection not in shoe_codes:
        print("Shoe not found")


def value_per_item():
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    # Iterate through each item and print the value
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        print(f"Value of {shoe.product}: {value}")


def highest_qty():
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    # extract the quantities of all the shoes in the inventory
    amounts = [shoe.get_quantity() for shoe in shoe_list]
    # find out the highest quantity
    highest_amount = max(amounts)

    # extract the index of the highest quantity shoe from shoe list. Ensures multiple highest quantity shoes are accounted for.
    indices = [i for i in range(len(amounts)) if amounts[i] == highest_amount]
    sale_shoes = []
    for index in indices:
        sale_shoes.append(shoe_list[index])

    # display shoes with the highest quantity and show as for sale
    print("Excess supply. The following shoes are for sale, half the stated price.\n")
    for shoe in sale_shoes:
        print(f"{shoe}\n")


# ==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''

# Read shoe stock data from the file.
read_shoes_data()

while True:
    # shoe menu
    print("\nWelcome to Stock Manager!\n")
    print("Menu")
    print("""
c   - Capture Shoe
v   - View Shoes
r   - Restock Shoe
s   - Search for Shoe
val - Value of Items
h   - Highest Supply, Put Shoe on Sale
e   - Exit
""")
    menu = input("Please select an option: ").lower()
    # menu options
    if menu == "c":
        capture_shoes()
    elif menu == "v":
        view_all()
    elif menu == "r":
        re_stock()
    elif menu == "s":
        search_shoe()
    elif menu == "val":
        value_per_item()
    elif menu == "h":
        highest_qty()
    elif menu == "e":
        print("Exiting...")
        exit()
    else:
        print("Invalid option")
