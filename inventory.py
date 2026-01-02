import json
import os

DATA_FILE = "data.json"
LOW_STOCK_LIMIT = 5


# ------------------ Product Entity ------------------
class Product:
    def __init__(self, product_id, name, quantity, price):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return (
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Qty: {self.quantity} | "
            f"Price: ₹{self.price}"
        )

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price
        }


# ------------------ Inventory Manager ------------------
class InventoryManager:
    def __init__(self):
        self.products = {}
        self.load_data()

    # ---------- File Handling ----------
    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as file:
                    data = json.load(file)
                    for pid, pdata in data.items():
                        self.products[pid] = Product(**pdata)
        except FileNotFoundError:
            print("Data file not found. Starting fresh.")
        except Exception as e:
            print("Error loading data:", e)

    def save_data(self):
        try:
            with open(DATA_FILE, "w") as file:
                json.dump(
                    {pid: p.to_dict() for pid, p in self.products.items()},
                    file,
                    indent=4
                )
            print("Data saved successfully.")
        except Exception as e:
            print("Error saving data:", e)

    # ---------- CRUD Operations ----------
    def add_product(self):
        try:
            product_id = input("Enter Product ID: ").strip()
            if product_id in self.products:
                print("❌ Product ID already exists.")
                return

            name = input("Enter Product Name: ").strip()
            if not name:
                raise ValueError("Name cannot be empty")

            quantity = int(input("Enter Quantity: "))
            price = float(input("Enter Price: "))

            self.products[product_id] = Product(product_id, name, quantity, price)
            print("✅ Product added successfully.")

        except ValueError:
            print("❌ Invalid input. Quantity and price must be numbers.")

    def view_products(self):
        if not self.products:
            print("No products available.")
            return

        for product in self.products.values():
            print(product)
            if product.quantity <= LOW_STOCK_LIMIT:
                print("⚠️ LOW STOCK ALERT!")

    def search_product(self):
        name = input("Enter product name to search: ").lower()
        found = False

        for product in self.products.values():
            if name in product.name.lower():
                print(product)
                found = True

        if not found:
            print("❌ Product not found.")

    def update_product(self):
        pid = input("Enter Product ID to update: ")
        try:
            product = self.products[pid]
            product.name = input("New Name: ") or product.name
            product.quantity = int(input("New Quantity: "))
            product.price = float(input("New Price: "))
            print("✅ Product updated.")
        except KeyError:
            print("❌ Product ID not found.")
        except ValueError:
            print("❌ Invalid input.")

    def delete_product(self):
        pid = input("Enter Product ID to delete: ")
        try:
            del self.products[pid]
            print("✅ Product deleted.")
        except KeyError:
            print("❌ Product ID not found.")

    # ---------- Stock Operations ----------
    def stock_update(self):
        pid = input("Enter Product ID: ")
        try:
            product = self.products[pid]
            choice = input("1. Stock In\n2. Stock Out\nChoose: ")

            qty = int(input("Enter quantity: "))
            if choice == "1":
                product.quantity += qty
            elif choice == "2":
                if qty > product.quantity:
                    print("❌ Insufficient stock.")
                    return
                product.quantity -= qty
            else:
                print("Invalid choice.")
                return

            print("✅ Stock updated.")

        except KeyError:
            print("❌ Product not found.")
        except ValueError:
            print("❌ Invalid quantity.")

    # ---------- Menu ----------
    def menu(self):
        while True:
            print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
            print("1. Add Product")
            print("2. View Products")
            print("3. Search Product")
            print("4. Update Product")
            print("5. Delete Product")
            print("6. Stock In / Out")
            print("7. Save & Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_product()
            elif choice == "2":
                self.view_products()
            elif choice == "3":
                self.search_product()
            elif choice == "4":
                self.update_product()
            elif choice == "5":
                self.delete_product()
            elif choice == "6":
                self.stock_update()
            elif choice == "7":
                self.save_data()
                print("👋 Exiting application.")
                break
            else:
                print("❌ Invalid choice.")


# ------------------ Run App ------------------
if __name__ == "__main__":
    manager = InventoryManager()
    manager.menu()
