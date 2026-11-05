# inventory.py
# A program that manages shoe stock using the data in inventory.txt


# ======== The Shoe class ========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        # Return the shoe's details as labelled lines of text
        return (f"Product:   {self.product}\n"
                f"Code:      {self.code}\n"
                f"Country:   {self.country}\n"
                f"Cost:      R{self.cost}\n"
                f"Quantity:  {self.quantity}")


# This list stores all the Shoe objects
shoe_list = []



def read_shoes_data():
    # Read inventory.txt and turn each line into a Shoe object
    shoe_list.clear()  # empty the list first so shoes are not added twice

    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: inventory.txt was not found.")
        return

    # lines[1:] skips the first line, which is the header
    for line in lines[1:]:
        try:
            country, code, product, cost, quantity = line.strip().split(",")
            shoe = Shoe(country, code, product, int(cost), int(quantity))
            shoe_list.append(shoe)
        except ValueError:
            print(f"Skipping a line with bad data: {line.strip()}")

    print(f"{len(shoe_list)} shoes loaded from inventory.txt.")


def save_shoes_data():
    # Write every shoe in the list back to inventory.txt
    with open("inventory.txt", "w") as file:
        file.write("Country,Code,Product,Cost,Quantity\n")
        for shoe in shoe_list:
            file.write(f"{shoe.country},{shoe.code},{shoe.product},"
                       f"{shoe.cost},{shoe.quantity}\n")


def get_number(message):
    # Keep asking until the user types a whole number of 0 or more
    while True:
        try:
            number = int(input(message))
            if number >= 0:
                return number
            print("The number cannot be negative.")
        except ValueError:
            print("Please enter a whole number.")


def capture_shoes():
    # Ask the user for a new shoe's details and add it to the list
    print("\n--- Add a new shoe ---")
    country = input("Country: ")
    code = input("Shoe code: ").upper()
    product = input("Product name: ")
    cost = get_number("Cost (R): ")
    quantity = get_number("Quantity: ")

    shoe_list.append(Shoe(country, code, product, cost, quantity))
    save_shoes_data()
    print(f"{product} has been added.")


def view_all():
    # Print every shoe using the __str__ method
    print("\n--- All shoes ---")
    for shoe in shoe_list:
        print(shoe)
        print("-" * 30)


def re_stock():
    # Find the shoe with the lowest quantity and offer to add more
    lowest = shoe_list[0]
    for shoe in shoe_list:
        if shoe.get_quantity() < lowest.get_quantity():
            lowest = shoe

    print("\n--- This shoe needs re-stocking ---")
    print(lowest)

    answer = input("Do you want to add stock? (yes/no): ").lower()
    if answer == "yes":
        amount = get_number("How many pairs do you want to add? ")
        lowest.quantity = lowest.quantity + amount
        save_shoes_data()
        print(f"{lowest.product} now has {lowest.quantity} pairs.")
    else:
        print("No stock was added.")


def search_shoe():
    # Find a shoe by its code and return it
    code = input("Enter the shoe code: ").upper()
    for shoe in shoe_list:
        if shoe.code == code:
            return shoe
    return None  # no shoe matched the code


def value_per_item():
    # Show the total value (cost * quantity) of each shoe
    print("\n--- Stock value per item ---")
    print(f"{'Product':<22}{'Cost':>8}{'Quantity':>10}{'Value':>12}")
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        print(f"{shoe.product:<22}{shoe.cost:>8}{shoe.quantity:>10}"
              f"{value:>12}")


def highest_qty():
    # Find the shoe with the highest quantity and show it as for sale
    highest = shoe_list[0]
    for shoe in shoe_list:
        if shoe.get_quantity() > highest.get_quantity():
            highest = shoe

    print("\n*** THIS SHOE IS FOR SALE ***")
    print(highest)


# Main menu
read_shoes_data()

while True:
    print("\n====== SHOE INVENTORY MENU ======")
    print("1 - View all shoes")
    print("2 - Add a shoe")
    print("3 - Search for a shoe")
    print("4 - Re-stock a shoe")
    print("5 - View stock value per item")
    print("6 - View the shoe for sale")
    print("0 - Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        view_all()
    elif choice == "2":
        capture_shoes()
    elif choice == "3":
        found_shoe = search_shoe()
        if found_shoe is None:
            print("No shoe found with that code.")
        else:
            print(found_shoe)
    elif choice == "4":
        re_stock()
    elif choice == "5":
        value_per_item()
    elif choice == "6":
        highest_qty()
    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Invalid option, please try again.")