import csv
from filehandler import read_csv, write_csv

Employee = "employees.csv"
Manager = "manager.csv"

def load_employees():
    return read_csv(Employee)

def save_employees(data):
    write_csv(Employee, data)

def load_managers():
    return read_csv(Manager)

def manager_login():
    managers = load_managers()
    print("Hello Manager! Please enter required credentials\n")
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        for m in managers:
            if m["username"] == username and m["password"] == password:
                print("\nLogin successful! Welcome", username)
                return True
        print("\nLogin failed! Invalid username or password. Please try again.\n")

def add_employee():
    employees = load_employees()
    num_of_employee = int(input("Enter number of employees to add: "))
    if num_of_employee <= 0:
        print("Error! Number of employees must be greater than zero.")
        return
    for i in range(1, num_of_employee + 1):
        print("Enter details for employee" , i)
        while True:
            id = int(input("Enter employee ID: "))
            if id <= 0:
                print("Error! Employee ID must be greater than zero.")
            else:
                is_exist = False
                for emp in employees:
                    if emp["ID"] == id:
                        is_exist = True
                        break
                if is_exist:
                    print("Error! Employee with this ID already exists.")
                else:
                    break

        name = input("Enter employee name: ")
        if name.strip() == "":
            print("Error! Employee name cannot be empty.")
            name = input("Enter employee name: ")
        elif name.isnumeric() or name.isdigit():
            print("Error! Employee name cannot be numeric.")
            name = input("Enter employee name: ")
        elif name[0].islower():
            print("Error! Employee name must start with an uppercase letter.")
            name = input("Enter employee name: ")
        for char in name:
            if char.isdigit():
                print("Error! Employee name cannot contain digits.")
                name = input("Enter employee name: ")
                break
            
        designation = input("Enter employee designation: ")
        if designation.strip() == "":
            print("Error! Employee designation cannot be empty.")
            designation = input("Enter employee designation: ")
        elif designation.isnumeric() or designation.isdigit():
            print("Error! Employee designation cannot be numeric.")
            designation = input("Enter employee designation: ")
        elif designation[0].islower():
            print("Error! Employee designation must start with an uppercase letter.")
            designation = input("Enter employee designation: ")
        for char in designation:
            if char.isdigit():
                print("Error! Employee designation cannot contain digits.")
                designation = input("Enter employee designation: ")
                break
            
        salary = input("Enter employee salary: ")
        while True:
            if salary.isalpha():
                print("Error! Employee salary cannot be alphabetic.")
                salary = input("Enter employee salary: ")
            elif float(salary) <= 0:
                print("Error! Employee salary must be greater than zero.")
                salary = input("Enter employee salary: ")
            else:
                salary = float(salary)
                break
        employee = {
            "ID": id ,
            "Name": name ,
            "Designation": designation ,
            "Salary": salary
        }
        employees.append(employee)
        print("\nEmployee added successfully!\n")
    save_employees(employees)

def update_employee():
    employees = load_employees()
    
    while True:
        id_to_update = input("Enter the employee ID to update: ")
        if id_to_update.isalpha():
            print("Error! Employee ID must be numeric.")
        elif int(id_to_update) <= 0:
            print("Error! Employee ID must be greater than zero.")
        else:
            id_to_update = int(id_to_update)
            break

    for emp in employees:
        if emp["ID"] == id_to_update:
            print("Current details of the employee:")
            for i , j in emp.items():
                print(f"{i}: {j}")
            to_update = input("What do you want to update (ID/Name/Designation/Salary): ")

            if to_update == "ID":
                while True:
                    new_id = input("Enter new ID: ")
                    if new_id.isalpha():
                        print("Error! ID must be numeric.")
                    elif int(new_id) <= 0:
                        print("Error! ID must be greater than zero.")
                    else:
                        exists = False
                        for e in employees:
                            if e["ID"] == int(new_id):
                                exists = True
                                break
                        if exists:
                            print("Error! Another employee with this ID already exists.")
                        else:
                            emp["ID"] = int(new_id)
                            print("ID updated successfully!")
                            break

            elif to_update == "Name":
                while True:
                    new_name = input("Enter new name: ")
                    if new_name.strip() == "":
                        print("Error! Name cannot be empty.")
                    elif new_name.isdigit():
                        print("Error! Name cannot be numeric.")
                    elif new_name[0].islower():
                        print("Error! Name must start with uppercase.")
                    else:
                        valid = True
                        for c in new_name:
                            if c.isdigit():
                                print("Error! Name cannot contain digits.")
                                valid = False
                                break
                        if valid:
                            emp["Name"] = new_name
                            print("Name updated successfully!")
                            break

            elif to_update == "Designation":
                while True:
                    new_designation = input("Enter new designation: ")
                    if new_designation.strip() == "":
                        print("Error! Designation cannot be empty.")
                    elif new_designation.isdigit():
                        print("Error! Designation cannot be numeric.")
                    elif new_designation[0].islower():
                        print("Error! Designation must start uppercase.")
                    else:
                        valid = True
                        for c in new_designation:
                            if c.isdigit():
                                print("Error! Designation cannot contain digits.")
                                valid = False
                                break
                        if valid:
                            emp["Designation"] = new_designation
                            print("Designation updated successfully!")
                            break

            elif to_update == "Salary":
                while True:
                    new_salary = input("Enter new salary: ")
                    if new_salary.isalpha():
                        print("Error! Salary cannot be alphabetic.")
                    elif float(new_salary) <= 0:
                        print("Error! Salary must be greater than zero.")
                    else:
                        emp["Salary"] = float(new_salary)
                        print("Salary updated successfully!")
                        break

            else:
                print("Error! Invalid choice")
                return

            save_employees(employees)
            print("\nEmployee updated successfully!")
            return

    print("Employee not found!")

def delete_employee():
    employees = load_employees()
    while True:
        id_to_delete = input("Enter the employee ID to delete: ")
        if id_to_delete.isalpha():
            print("Error! Employee ID must be numeric.")
        elif int(id_to_delete) <= 0:
            print("Error! Employee ID must be greater than zero.")
        else:
            id_to_delete = int(id_to_delete)
            break
    for emp in employees:
        if int(emp["ID"]) == id_to_delete:
            employees.remove(emp)
            print("\nEmployee deleted successfully!")
            save_employees(employees)
            return
    print("Employee not found!\n")

def view_employees_records():
    employees = load_employees()
    if not employees:
        print("No employee records found!\n")
    else:
        print("\nEmployee Records:")
        for emp in employees:
            for i, j in emp.items():
                print(f"{i}: {j}")
            print("-----------------------")

def assign_employee_designation():
    employees = load_employees()
    id_to_assign = int(input("Enter the employee ID to assign designation: "))
    for emp in employees:
        if int(emp["ID"]) == id_to_assign:
            print("Current Designation:", emp["Designation"])
            new_designation = input("Enter new designation to assign: ")
            emp["Designation"] = new_designation
            print("\nDesignation assigned successfully!")
            save_employees(employees)
            return
    print("Error! Employee not found!\n")

def search_employee():
    employees = load_employees()
    print("\nSearch Employee Options:")
    print("1. Search by ID")
    print("2. Search by Name")
    print("3. Search by Designation")
    choice = input("Enter your choice): ")
    if choice == "1":
        search_id = int(input("Enter Employee ID to search: "))
        found = False
        for emp in employees:
            if int(emp["ID"]) == search_id:
                print(f"ID: {emp['ID']}, Name: {emp['Name']}, Designation: {emp['Designation']}")
                found = True
        if not found:
            print("No employee found with this ID.")
    elif choice == "2":
        search_name = input("Enter Employee Name to search: ")
        found = False
        for emp in employees:
            if emp["Name"].lower() == search_name.lower():
                print(f"ID: {emp['ID']}, Name: {emp['Name']}, Designation: {emp['Designation']}")
                found = True
        if not found:
            print("No employee found with this Name.")
    elif choice == "3":
        search_role = input("Enter Employee Designation to search: ")
        found = False
        for emp in employees:
            if emp["Designation"].lower() == search_role.lower():
                print(f"ID: {emp['ID']}, Name: {emp['Name']}, Designation: {emp['Designation']}")
                found = True
        if not found:
            print("No employee found with this Designation.")
    else:
        print("Invalid choice!")