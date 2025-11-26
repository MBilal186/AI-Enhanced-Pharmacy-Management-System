from utils.filehandling import read_csv, write_csv

Customer = "database/customers.csv"
customers = []

def load_customers():
    global customers
    customers = read_csv(Customer)

def save_customers():
    write_csv(Customer, customers)

def add_customer():
    load_customers()
    print("\n--- Add Customer ---")

    invoice = input("Enter Invoice Number: ")
    if invoice.strip() == "":
        print("Error! Invoice cannot be empty.")
        invoice = input("Enter Invoice Number: ")

    phone = input("Enter Phone Number: ")
    if phone.strip() == "" or not phone.isdigit():
        print("Error! Phone must be numeric and not empty.")
        phone = input("Enter Phone Number: ")

    name = input("Enter Customer Name: ")
    if name.strip() == "":
        print("Error! Name cannot be empty.")
        name = input("Enter Customer Name: ")
    elif name.isdigit():
        print("Error! Name cannot be numeric.")
        name = input("Enter Customer Name: ")
    elif name[0].islower():
        print("Error! Name must start with uppercase.")
        name = input("Enter Customer Name: ")

    for ch in name:
        if ch.isdigit():
            print("Error! Name cannot contain digits.")
            name = input("Enter Customer Name: ")
            break

    item = input("Medicine Purchased: ")
    if item.strip() == "":
        print("Error! Item cannot be empty.")
        item = input("Medicine Purchased: ")

    qty = input("Quantity: ")
    if qty.isdigit():
        if int(qty) > 0:
            qty = int(qty)
        else:
            print("Error! Quantity must be a positive number.")
            qty = input("Quantity: ")
            qty = int(qty)
    else:
        print("Error! Quantity must be a positive number.")
        qty = input("Quantity: ")
        qty = int(qty)

    price = input("Price per item: ")
    if not price.isdigit() or int(price) <= 0:
        print("Error! Price must be a positive number.")
        price = input("Price per item: ")
    price = int(price)

    total = qty * price
    cid = str(len(customers))

    new_row = [cid, name, phone, invoice, item, qty, price, total]
    customers.append(new_row)
    save_customers()

    print("\nCustomer Added Successfully!\n")

def view_customers():
    load_customers()
    if not customers:
        print("No customer records found!\n")
    else:
        print("\n--- Customer Records ---")
        for row in customers:
            for value in row:
                print(value, end=" | ")
            print("\n-----------------------")

def delete_customer():
    load_customers()
    invoice = input("Enter Invoice Number to delete: ")

    found = False
    for row in customers:
        if invoice == row[3]:
            customers.remove(row)
            save_customers()
            found = True
            print("\nCustomer Deleted Successfully!\n")
            break

    if not found:
        print("Customer Not Found!\n")

def search_customer():
    load_customers()
    print("Search By: 1. Invoice 2. Phone")
    choice = input("Enter choice: ")

    if choice == "1":
        invoice = input("Enter Invoice Number: ")
        found = False
        for row in customers:
            if invoice == row[3]:
                print("\nCustomer Found:")
                for x in row:
                    print(x, end=" | ")
                print()
                found = True
        if not found:
            print("Customer Not Found!")

    elif choice == "2":
        phone = input("Enter Phone Number: ")
        found = False
        for row in customers:
            if phone == row[2]:
                print("\nCustomer Found:")
                for x in row:
                    print(x, end=" | ")
                print()
                found = True
        if not found:
            print("Customer Not Found!")

    else:
        print("Invalid choice!")

def generate_bill():
    item = input("Medicine Name: ")

    qty = input("Quantity: ")
    if not qty.isdigit() or int(qty) <= 0:
        print("Error! Quantity must be positive.")
        qty = input("Quantity: ")
    qty = int(qty)

    price = input("Price per item: ")
    if not price.isdigit() or int(price) <= 0:
        print("Error! Price must be positive.")
        price = input("Price per item: ")
    price = int(price)

    total = qty * price

    print("\n--- BILL ---")
    print(f"Item: {item} | Quantity: {qty} | Price: {price} | Total: {total}")

def apply_discount():
    total = input("Enter total bill amount: ")
    if not total.isdigit() or int(total) <= 0:
        print("Error! Total must be positive.")
        total = input("Enter total bill amount: ")
    total = int(total)

    print("Discount Options: 1. 10% 2. 20% 3. 30%")
    choice = input("Select discount: ")

    discount = 0

    if choice == "1":
        discount = total * 0.1
    elif choice == "2":
        discount = total * 0.2
    elif choice == "3":
        discount = total * 0.3
    else:
        print("Invalid choice!")
    final = total - discount
    print(f"Original: {total} | Discount: {discount} | Final Amount: {final}")