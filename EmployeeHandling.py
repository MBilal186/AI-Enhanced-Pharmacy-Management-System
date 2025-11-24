employees = []

def add_employee():
    num_of_employee = int(input("Enter number of employees to add: "))
    if num_of_employee <= 0:
        print("Error! Number of employees must be greater than zero.")
    else:
        for i in range(1 , num_of_employee+1):
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

            salary = float(input("Enter employee salary: "))
            if salary <= 0:
                print("Error! Employee salary must be greater than zero.")
                salary = float(input("Enter employee salary: "))
            elif salary.isalpha():
                print("Error! Employee salary cannot be alphabetic.")
                salary = float(input("Enter employee salary: "))

            employee = {
                "ID": id ,
                "Name": name,
                "Designation": designation,
                "Salary": salary
            }
            employees.append(employee)
            print("\nEmployee added successfully!\n")

def update_employee():
    id_to_update = input("Enter the employee ID to update: ")
    if id_to_update.isalpha():
        print("Error! Employee ID must be numeric.")
        id_to_update = int(input("Enter the employee ID to update: "))
        return
    elif id_to_update <= 0:
        print("Error! Employee ID must be greater than zero.")
        id_to_update = int(input("Enter the employee ID to update: "))
        return
    else:
        for emp in employees:
            if emp["ID"] == id_to_update:
                print("Current details of the employee:")
                for i,j in emp.items():
                    print(f"{i}: {j}")
                to_update = input("What do you want to update (ID or Name or Designation or Salary): ")
                if to_update == "ID":
                    new_id = input("Enter new ID: ")
                    emp["ID"] = new_id
                    print("ID updated successfully!")
                elif to_update == "Name":
                    new_name = input("Enter new name: ")
                    emp["Name"] = new_name
                    print("Name updated successfully!")
                elif to_update == "Designation":
                    new_designation = input("Enter new designation: ")
                    emp["Designation"] = new_designation
                    print("Designation updated successfully!")
                elif to_update == "Salary":
                    new_salary = input("Enter new salary: ")
                    emp["Salary"] = new_salary
                    print("Salary updated successfully!")
                else:
                    print("Erro! Invalid choice")
                print("\nEmployee updated successfully!")
                return
        else:
            print("Employee not found!")

def delete_employee():
    id_to_delete = int(input("Enter the employee ID to delete: "))
    if id_to_delete <= 0:
        print("Error! Employee ID must be greater than zero.")
        return
    elif id_to_delete.isalpha():
        print("Error! Employee ID must be numeric.")
        return
    for emp in employees:
        if emp["ID"] == id_to_delete:
            employees.remove(emp)
            print("\nEmployee deleted successfully!")
            return
    else:
        print("Employee not found!\n")

def view_employees_records():
    if not employees:
        print("No employee records found!\n")
    else:
        print("\nEmployee Records:")
        for emp in employees:
            for i,j in emp.items():
                print(f"{i}: {j}")
            print("-----------------------")

def assign_employee_designation():
    id_to_assign = int(input("Enter the employee ID to assign designation: "))
    if id_to_assign <= 0:
        print("Error! Employee ID must be greater than zero.")
        return
    elif id_to_assign.isalpha():
        print("Error! Employee ID must be numeric.")
        return
    for emp in employees:
        if emp["ID"] == id_to_assign:
            print("Current Designation:", emp["Designation"])
            new_designation = input("Enter new designation to assign: ")
            emp["Designation"] = new_designation
            print("\nDesignation assigned successfully!")
            return
    else:
        print("Error! Employee not found!\n")
