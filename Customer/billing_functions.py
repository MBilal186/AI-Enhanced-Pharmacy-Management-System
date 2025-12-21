# billing_functions.py
from datetime import datetime
from utils.filehandler import read_csv, write_csv
from Medicine.medicine_functions import load_medicines, reduce_stock

SALES_FILE = "dataset/sales.csv"


def get_available_medicines():
    """
    Returns medicine list from CSV
    """
    return load_medicines()


def calculate_cart_totals(cart_items):
    """
    cart_items = [
        {"id": "1", "name": "Panadol", "qty": 2, "price": 50}
    ]
    """
    subtotal = 0
    for item in cart_items:
        subtotal += float(item["price"]) * int(item["qty"])
    return subtotal


def finalize_sale(customer_name, cart_items):
    """
    Finalizes ONE bill with multiple medicines
    """
    if not cart_items:
        return False, "Cart is empty"

    # 1Check stock availability FIRST
    for item in cart_items:
        success = reduce_stock(item["name"], int(item["qty"]))
        if not success:
            return False, f"Not enough stock for {item['name']}"

    # 2️Load existing sales
    try:
        sales = read_csv(SALES_FILE)
    except FileNotFoundError:
        sales = [
            ["sale_id", "customer", "medicine", "qty", "price", "total", "date"]
        ]

    sale_id = len(sales)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 3️Save each medicine as part of SAME bill
    for item in cart_items:
        total = float(item["price"]) * int(item["qty"])
        row = [
            sale_id,
            customer_name,
            item["name"],
            item["qty"],
            item["price"],
            total,
            date
        ]
        sales.append(row)

    write_csv(SALES_FILE, sales)
    return True, sale_id
