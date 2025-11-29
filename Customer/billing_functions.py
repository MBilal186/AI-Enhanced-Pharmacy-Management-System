import csv
from datetime import datetime
from utils.filehandler import read_csv, write_csv
from Medicine.medicine_functions import reduce_stock, load_medicines

Sales_file = "Customer/sales.csv"
def view_available_medicines():
    data = load_medicines()
    print("\n--- Available Medicines ---")
    for row in data:
        print(f"{row[1]} | Price: Rs.{row[2]} | Stock: {row[3]} | Exp: {row[4]}")
    print()

def buy_medicine():
    data = load_medicines()
    customer = input("Enter customer name : ")
    medicine_name = input("Enter medicine name : ").lower()
    qty = int(input("Enter Quantity : "))
    for med in data:
        if medicine_name in med[1].lower():
            price = float(med[2])
            total = price * qty
            print(f"\nMedicine : {med[1]}")
            print(f"Price per unit : Rs.{price}")
            print(f"Total : Rs.{total}") 

            reduce_stock(med[1],qty)
            save_sale(customer, med[1], qty, price, total)
            print_bill(customer, med[1], qty, price, total)
            return
        
    print("Medicine not found!")
            
def save_sale(customer, medicine_name, qty, price, total):
    try:
        sales = read_csv(Sales_file)
    except FileNotFoundError:
        sales = [["sale_id", "customer_name", "medicine_name", "quantity", "price", "total", "date"]]

    sale_id = len(sales)
    date = datetime.now().strftime("%Y-%m-%d")

    new_row = [sale_id, customer, medicine_name, qty, price, total, date]
    sales.append(new_row)
    write_csv(Sales_file, sales)
    print("\nSale recorded successfully!")

def print_bill(customer, medicine, qty, price, total):
    print("\n====== BILL ======")
    print(f"Customer: {customer}")
    print(f"Medicine: {medicine}")
    print(f"Quantity: {qty}")
    print(f"Price per unit: Rs.{price}")
    print(f"Total Amount: Rs.{total}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==========================\n")

def view_sales_history():
    try:
        data = read_csv(Sales_file)
        print("\n--- SALES HISTORY ---")
        for row in data:
            print(row)
    except FileNotFoundError:
        print("\nNo sales record found.")