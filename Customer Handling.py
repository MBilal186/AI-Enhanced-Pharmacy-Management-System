import csv
from filehandler import read_csv, write_csv

Customer_File = "customers.csv"

def load_customers():
    return read_csv(Customer_File)

def save_customers(data):
    write_csv(Customer_File, data)

def add_customer():
    customers = load_customers()

    num_customers = input("Enter number of customers to add: ")
    while not num_customers.isdigit() or int(num_customers) <= 0:
        print("Error! Number must be a positive integer.")
        num_customers = input("Enter number of customers to add: ")

    num_customers = int(num_customers)

    for i in range(1, num_customers + 1):
        print(f"\nEnter details for customer {i}")

        # Customer ID
        while True:
            cid = input("Enter customer ID: ")
            if not cid.isdigit() or int(cid) <= 0:
                print("Error! Customer ID must be numeric and greater than zero.")
                continue

            cid = int(cid)
            exists = False
            for c in customers:
                if c["ID"] == cid:
                    exists = True
                    break
            if exists:
                print("Error! Customer with this ID already exists.")
            else:
                break

        # Customer Name
        while True:
            name = input("Enter customer name: ")
            if name.strip() == "":
                print("Error! Name cannot be empty.")
            elif name.isdigit():
                print("Error! Name cannot be numbers.")
            elif name[0].islower():
                print("Error! Name must start with uppercase.")
            else:
                valid = True
                for ch in name:
                    if ch.isdigit():
                        valid = False
                        print("Error! Name cannot contain digits.")
                        break
                if valid:
                    break

        # Contact Number
        while True:
            contact = input("Enter customer phone number: ")
            if not contact.isdigit():
                print("Error! Contact number must be numeric.")
            elif len(contact) < 10:
                print("Error! Contact must contain at least 10 digits.")
            else:
                break

        # Address
        while True:
            address = input("Enter customer address: ")
            if address.strip() == "":
                print("Error! Address cannot be empty.")
            else:
                break

        customer = {
            "ID": cid,
            "Name": name,
            "Contact": contact,
            "Address": address
        }

        customers.append(customer)
        print("Customer added successfully!\n")

    save_customers(customers)


def update_customer():
    customers = load_customers()

    while True:
        cid = input("Enter the customer ID to update: ")
        if not cid.isdigit() or int(cid) <= 0:
            print("Error! Customer ID must be numeric and greater than zero.")
        else:
            cid = int(cid)
            break

    for c in customers:
        if c["ID"] == cid:
            print("\nCurrent customer details:")
            for key, val in c.items():
                print(f"{key}: {val}")

            field = input("\nWhat do you want to update (ID/Name/Contact/Address): ")

            # Update ID
            if field == "ID":
                while True:
                    new_id = input("Enter new ID: ")
                    if not new_id.isdigit() or int(new_id) <= 0:
                        print("Error! ID must be numeric and greater than zero.")
                    else:
                        new_id = int(new_id)
                        exists = False
                        for cc in customers:
                            if cc["ID"] == new_id:
                                exists = True
                                break
                        if exists:
                            print("Error! Another customer with this ID already exists.")
                        else:
                            c["ID"] = new_id
                            print("Customer ID updated successfully!")
                            break

            # Update Name
            elif field == "Name":
                while True:
                    new_name = input("Enter new name: ")
                    if new_name.strip() == "":
                        print("Error! Name cannot be empty.")
                    elif new_name.isdigit():
                        print("Error! Name cannot be digits.")
                    elif new_name[0].islower():
                        print("Error! Name must start uppercase.")
                    else:
                        valid = True
                        for ch in new_name:
                            if ch.isdigit():
                                print("Error! Name cannot contain digits.")
                                valid = False
                                break
                        if valid:
                            c["Name"] = new_name
                            print("Name updated successfully!")
                            break

            # Update Contact
            elif field == "Contact":
                while True:
                    new_contact = input("Enter new contact: ")
                    if not new_contact.isdigit():
                        print("Error! Contact must be numeric.")
                    elif len(new_contact) < 10:
                        print("Error! Contact must contain at least 10 digits.")
                    else:
                        c["Contact"] = new_contact
                        print("Contact updated successfully!")
                        break

            # Update Address
            elif field == "Address":
                while True:
                    new_addr = input("Enter new address: ")
                    if new_addr.strip() == "":
                        print("Error! Address cannot be empty.")
                    else:
                        c["Address"] = new_addr
                        print("Address updated successfully!")
                        break

            else:
                print("Invalid update field!")
                return

            save_customers(customers)
            print("\nCustomer updated successfully!")
            return

    print("Customer not found!")


def delete_customer():
    customers = load_customers()

    while True:
        cid = input("Enter the customer ID to delete: ")
        if not cid.isdigit() or int(cid) <= 0:
            print("Error! Customer ID must be numeric and positive.")
        else:
            cid = int(cid)
            break

    for c in customers:
        if c["ID"] == cid:
            customers.remove(c)
            save_customers(customers)
            print("Customer deleted successfully!\n")
            return

    print("Customer not found!\n")


def view_customers():
    customers = load_customers()
    if not customers:
        print("\nNo customer records found!\n")
        return

    print("\nCustomer Records:")
    for c in customers:
        for key, val in c.items():
            print(f"{key}: {val}")
        print("---------------------------")


def search_customer():
    customers = load_customers()

    print("\nSearch Customer Options:")
    print("1. Search by ID")
    print("2. Search by Name")
    print("3. Search by Contact")

    choice = input("Enter your choice: ")

    # Search by ID
    if choice == "1":
        sid = input("Enter customer ID: ")
        if not sid.isdigit():
            print("Invalid ID format.")
            return
        sid = int(sid)

        found = False
        for c in customers:
            if c["ID"] == sid:
                print(c)
                found = True
        if not found:
            print("Customer not found.")

    # Search by Name
    elif choice == "2":
        sname = input("Enter customer name: ")
        found = False
        for c in customers:
            if c["Name"].lower() == sname.lower():
                print(c)
                found = True
        if not found:
            print("Customer not found.")

    # Search by Contact
    elif choice == "3":
        scontact = input("Enter contact number: ")
        found = False
        for c in customers:
            if c["Contact"] == scontact:
                print(c)
                found = True
        if not found:
            print("Customer not found.")

    else:
        print("Invalid choice!")
