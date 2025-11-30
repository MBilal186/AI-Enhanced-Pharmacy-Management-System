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
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    for m in managers:
        if m["username"] == username and m["password"] == password:
            print("\nLogin successful! Welcome", username)
            return True
    print("\nLogin failed! Invalid username or password.\n")
    return False

def add_employee():
    employees = load_employees()
    num_of_employee = int(input("Enter number of employees to add: "))
    if num_of_employee <= 0:
        print("Error! Number of employees must be greater than zero.")
        return
    for i in range(1, num_of_employee + 1):
        print("Enter details for employee", i)
        while True:
            id = int(input("Enter employee ID: "))
            if id <= 0:
                print("Error! Employee ID must be greater than zero.")
            elif any(int(emp["ID"]) == id for emp in employees):
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
        employee = {"ID": id, "Name": name, "Designation": designation, "Salary": salary}
        employees.append(employee)
        print("\nEmployee added successfully!\n")
    save_employees(employees)

def update_employee():
    employees = load_employees()
    id_to_update = input("Enter the employee ID to update: ")
    for emp in employees:
        if str(emp["ID"]) == id_to_update:
            print("Current details of the employee:")
            for i, j in emp.items():
                print(f"{i}: {j}")
            to_update = input("What do you want to update (ID/Name/Designation/Salary): ")
            if to_update in emp:
                new_value = input(f"Enter new {to_update}: ")
                if to_update == "ID":
                    new_value = int(new_value)
                elif to_update == "Salary":
                    new_value = float(new_value)
                emp[to_update] = new_value
                print(f"{to_update} updated successfully!")
            else:
                print("Error! Invalid choice.")
            save_employees(employees)
            return
    print("Employee not found!")

def delete_employee():
    employees = load_employees()
    id_to_delete = int(input("Enter the employee ID to delete: "))
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
    choice = input("Enter choice (1/2/3): ")
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