from customer import add_customer, view_customers, delete_customer, search_customer, generate_bill, apply_discount

while True:
    print("\n========= CUSTOMER MANAGEMENT SYSTEM =========")
    print("1. Add Customer")
    print("2. View All Customers")
    print("3. Delete Customer")
    print("4. Search Customer")
    print("5. Generate Bill")
    print("6. Apply Discount")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_customer()
    elif choice == "2":
        view_customers()
    elif choice == "3":
        delete_customer()
    elif choice == "4":
        search_customer()
    elif choice == "5":
        generate_bill()
    elif choice == "6":
        apply_discount()
    elif choice == "7":
        print("Exiting...")
        break
    else:
        print("Invalid choice! Try again.")