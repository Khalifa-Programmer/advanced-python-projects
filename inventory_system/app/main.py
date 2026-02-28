
from database.models import create_tables
from services.inventory_service import InventoryService
from utils.csv_exporter import export_to_csv

def main():
    create_tables()
    service = InventoryService()
    while True:
        print("\n1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Export CSV")
        print("6. Exit")
        choice = input("Choose: ")
        if choice == "1":
            name = input("Name: ")
            quantity = int(input("Quantity: "))
            price = float(input("Price: "))
            service.add_product(name, quantity, price)
        elif choice == "2":
            products = service.view_products()
            for p in products:
                print(p)
        elif choice == "3":
            pid = int(input("Product ID: "))
            quantity = int(input("New Quantity: "))
            price = float(input("New Price: "))
            service.update_product(pid, quantity, price)
        elif choice == "4":
            pid = int(input("Product ID: "))
            service.delete_product(pid)
        elif choice == "5":
            export_to_csv(service.view_products())
            print("CSV Exported!")
        elif choice == "6":
            break

if __name__ == "__main__":
    main()
