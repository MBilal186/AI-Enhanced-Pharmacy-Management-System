from utils.filehandler import read_csv, write_csv
from datetime import datetime

MEDICINE_FILE = "dataset/medicine.csv"
def load_medicines():
    return read_csv(MEDICINE_FILE)

def save_medicines(data):
    write_csv(MEDICINE_FILE, data)

def view_medicines():
    data = load_medicines()
    print("\n---Medicines List---")
    for row in data:
        print(row)

def search_medicine():
    data = load_medicines
    name = input("Enter medicine name you want to search : ").lower()
    for row in data:
        if name in row[1].lower():
            print("\nMedicine Found!")
            print(row)
            return
    print("\nMedicine not found!")

def add_medicine():
    data = load_medicines()
    print("\nEnter new medicine details : ")
    id = str(len(data))
    name = input("Name : ")
    price = float(input("Price : "))
    qty = int(input("Quantity : "))
    exp = input("Expiry (YYYY-MM-DD) : ")

    new_row = [id, name, price, qty, exp]
    data.append(new_row)
    save_medicines(data)
    print("\nMedicine Added Successfully!")

def update_medicine():
    data = load_medicines()
    name = input("Enter medicine name to update : ").lower()
    for i in range(len(data)):
        if name in data[i][1].lower():
            print("\nMedicine Found : ",data[i])
            print("Enter new values (leave empty to keep old) : ")
            new_name = input(f"New Name [{data[i][1]}] : ") or data[i][1]
            new_price = input(f"New Price [{data[i][2]}] : ") or data[i][2]
            new_qty = input(f"New Quantity [{data[i][3]}] : ") or data[i][3]
            new_exp = input(f"New Expiry [{data[i][4]}] : ") or data[i][4]

            data[i] = [data[i][0], new_name, new_price, new_qty, new_exp]
            save_medicines(data)
            print("\nMedicine Updated Successfully!")
            return
    
    print("\nMedicine not found!")

def delete_medicine():
    data = load_medicines()
    name = input("Enter medicine name to delete : ").lower()
    new_data = []
    found = False
    for row in data:
        if name in row[1].lower():
            found = True
            continue
        new_data.append(row)

    if found:
        save_medicines(new_data)
        print("\nMedicine deleted successfully!")
    else:
        print("\nMedicine not found!")

def delete_expired_medicines():
    data = load_medicines()
    today = datetime.today.date()
    new_data = []
    removed = False
    for row in data:
        expiry_date = datetime.strptime(row[4], "%Y-%m-%d").date()

        if expiry_date < today:
            print(f"Expired Removed : {row}")
            removed = True
        else:
            new_data.append(row)
    
    save_medicines(new_data)
    if removed:
        print("\nExpired medicines deleted!")
    else:
        print("\nNo expired medicines found.")

def check_expiring_soon():
    data = load_medicines()
    today = datetime.today.date()
    print("\n---Medicines Expiring Soon (Within 30 Days)---")
    found = False
    for row in data:
        expiry = datetime.strptime(row[4], "%Y-%m-%d").date()
        days_left = (expiry - today).days

        if 0 < days_left <=30:
            print(f"{row[1]} | Expires in {days_left} days")
            found = True

    if not found:
        print("No medicines expiring soon.")

def reduce_stock(medicine_name, qty):
    data = load_medicines()
    for i in range(len(data)):
        if medicine_name.lower() in data[i][1].lower():
            current_qty = int(data[i][3])
            if current_qty < qty:
                print("Not enough stock available!")
                return False

            data[i][3] = str(current_qty - qty)
            save_medicines(data)
            print(f"Stock updated: {medicine_name} - {qty} sold")
            return True

    print("Medicine not found!")
    return False

def ai_recommend():
    sym = input("Enter your symptoms: ").lower()
    print("\n--- AI Recommendation ---")
    if "fever" in sym:
        print("Recommended: Panadol / Paracetamol")
    elif "pain" in sym or "headache" in sym:
        print("Recommended: Brufen / Ibuprofen")
    elif "cough" in sym:
        print("Recommended: Brodin / Cough Syrup")
    elif "flu" in sym or "cold" in sym:
        print("Recommended: Antiflu / Panadol Cold")
    elif "allergy" in sym or "rash" in sym:
        print("Recommended: Cetirizine / Allergex")
    else:
        print("No exact match found. Please consult a pharmacist.")