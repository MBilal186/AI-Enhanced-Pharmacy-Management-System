from Medicine.medicine_functions import (
    view_medicines, search_medicine, add_medicine,
    update_medicine, delete_medicine, delete_expired_medicines,
    check_expiring_soon, reduce_stock, ai_recommend
)

while True:
    print("\n===== MEDICINE MANAGEMENT SYSTEM =====")
    print("1. View Medicines")
    print("2. Search Medicine")
    print("3. Add Medicine")
    print("4. Update Medicine")
    print("5. Delete Medicine")
    print("6. Delete Expired Medicines")
    print("7. Check Expiring Soon")
    print("8. Reduce Stock (Sale)")
    print("9. AI Recommendation")
    print("10. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        view_medicines()
    elif choice == "2":
        search_medicine()
    elif choice == "3":
        add_medicine()
    elif choice == "4":
        update_medicine()
    elif choice == "5":
        delete_medicine()
    elif choice == "6":
        delete_expired_medicines()
    elif choice == "7":
        check_expiring_soon()
    elif choice == "8":
        name = input("Medicine name: ")
        qty = int(input("Quantity: "))
        reduce_stock(name, qty)
    elif choice == "9":
        ai_recommend()
    elif choice == "10":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")
print("Welcome to pharmacy")
