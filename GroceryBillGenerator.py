import tkinter as tk

class GroceryShop:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Shop")
        self.root.geometry("800x450")
        self.cart = {}
        self.total_price = 0

        self.item_frame = tk.Frame(root)
        self.item_frame.pack(side=tk.LEFT)

        self.cart_frame = tk.Frame(root)
        self.cart_frame.pack(side=tk.RIGHT)
        self.item_prices = {
            "Toor dal": 80,
            "Maysure dal": 30,
            "Milk": 54,
            "Bread": 40,
            "Wheat": 50,
            "bajri": 56,
            "jowari": 60,
            "Moong dal": 45,
            "Rice": 45,
            "Sugar": 40,
            "Salt": 40,
            "Corn flour": 45,
            "Wheat flour": 50,
            "All purpose flour": 52,
            "Rice flour": 42
        }
        self.display_grocery_items()

        self.custom_item_window = None
        self.custom_item_name_entry = None
        self.custom_item_price_entry = None
        self.custom_item_quantity_entry = None

        self.row_index = 1  # Initialize the row index for cart items

        self.add_custom_item_button = None
        self.generate_bill_button = None

        self.create_buttons_frame()  # Create a frame for buttons
        self.display_buttons()  # Display the buttons

        self.display_cart()
        self.search_frame = tk.Frame(root)
        self.search_frame.pack(side=tk.TOP)
        self.search_label = tk.Label(self.search_frame, text="Search Item:")
        self.search_label.grid(row=0, column=0)
        self.search_entry = tk.Entry(self.search_frame, width=20)
        self.search_entry.grid(row=0, column=1)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_items)
        self.search_button.grid(row=0, column=2)

        self.display_grocery_items()

    def search_items(self):
            keyword = self.search_entry.get()
            if keyword:
                # Filter and display only items that contain the keyword
                filtered_items = {item: price for item, price in self.item_prices.items() if keyword.lower() in item.lower()}
                self.display_grocery_items(filtered_items)
            else:
                # If the search bar is empty, display all items
                self.display_grocery_items(self.item_prices)
                
    def add_to_cart(self, item_name, item_price, quantity=1):
        if item_name in self.cart:
            self.cart[item_name]['quantity'] += quantity
        else:
            self.cart[item_name] = {'quantity': quantity, 'price': item_price}
        self.total_price += item_price * quantity
        self.display_cart()

    def remove_from_cart(self, item_name):
        if item_name in self.cart:
            item_info = self.cart[item_name]
            if item_info['quantity'] > 1:
                item_info['quantity'] -= 1
            else:
                del self.cart[item_name]
            self.total_price -= item_info['price']
            self.display_cart()

    def generate_bill(self, discount_percentage):
        bill_window = tk.Toplevel(self.root)
        bill_window.title("Bill")
        bill_window.geometry("400x300")
        bill_text = "Item\tQuantity\tPrice\n"
        for item, info in self.cart.items():
            bill_text += f"{item}\t{info['quantity']}\t{info['quantity'] * info['price']:.2f}\n"
        discount = (discount_percentage / 100) * self.total_price
        bill_text += f"Subtotal: {self.total_price:.2f}\n"
        bill_text += f"Discount: {discount:.2f}\n"
        bill_text += f"Total Price: {self.total_price - discount:.2f}"
        bill_label = tk.Label(bill_window, text=bill_text)
        bill_label.pack()

    def display_grocery_items(self, items=None):
            if items is None:
                items = self.item_prices

            for widget in self.item_frame.winfo_children():
                widget.destroy()

            for item, price in items.items():
                item_frame = tk.Frame(self.item_frame)
                item_frame.pack()
                item_label = tk.Label(item_frame, text=f"{item} - Rs{price:.2f}")
                item_label.pack()
                add_to_cart_button = tk.Button(item_frame, text="Add to Cart", command=lambda item=item, price=price: self.add_to_cart(item, price))
                add_to_cart_button.pack()

    def display_cart(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        cart_label = tk.Label(self.cart_frame, text="Your Cart:")
        cart_label.grid(row=0, column=0, columnspan=3)

        for item, info in self.cart.items():
            cart_item_label = tk.Label(self.cart_frame, text=f"{item} x{info['quantity']} - Rs{info['price']:.2f}")
            cart_item_label.grid(row=self.row_index, column=0, columnspan=2)

            remove_button = tk.Button(self.cart_frame, text="Remove", command=lambda item=item: self.remove_from_cart(item))
            remove_button.grid(row=self.row_index, column=2)
            self.row_index += 1

    def create_buttons_frame(self):
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(side=tk.RIGHT)

    def display_buttons(self):
        # Buttons for adding a custom item and generating a bill
        if self.add_custom_item_button is None:
            self.add_custom_item_button = tk.Button(self.buttons_frame, text="Add Custom Item", command=self.add_custom_item_window)
            self.add_custom_item_button.pack()

        if self.generate_bill_button is None:
            self.generate_bill_button = tk.Button(self.buttons_frame, text="Generate Bill", command=self.get_discount)
            self.generate_bill_button.pack()

    def add_custom_item_window(self):
        if self.custom_item_window:
            self.custom_item_window.deiconify()
        else:
            self.custom_item_window = tk.Toplevel(self.root)
            self.custom_item_window.title("Add Custom Item")
            self.custom_item_window.geometry("300x150")

            custom_item_label = tk.Label(self.custom_item_window, text="Custom Item Details:")
            custom_item_label.pack()

            custom_item_name_label = tk.Label(self.custom_item_window, text="Name:")
            custom_item_name_label.pack()
            self.custom_item_name_entry = tk.Entry(self.custom_item_window, width=20)
            self.custom_item_name_entry.pack()

            custom_item_price_label = tk.Label(self.custom_item_window, text="Cost of Single Item (Rs):")
            custom_item_price_label.pack()
            self.custom_item_price_entry = tk.Entry(self.custom_item_window, width=10)
            self.custom_item_price_entry.pack()

            custom_item_quantity_label = tk.Label(self.custom_item_window, text="No. of Items:")
            custom_item_quantity_label.pack()
            self.custom_item_quantity_entry = tk.Entry(self.custom_item_window, width=5)
            self.custom_item_quantity_entry.pack()

            add_custom_item_button = tk.Button(self.custom_item_window, text="Add to Cart", command=self.add_custom_item_to_cart)
            add_custom_item_button.pack()

    def add_custom_item_to_cart(self):
        name = self.custom_item_name_entry.get()
        price = self.custom_item_price_entry.get()
        quantity = self.custom_item_quantity_entry.get()

        try:
            price = float(price)
            quantity = int(quantity)
            if name and price > 0 and quantity > 0:
                self.add_to_cart(name, price, quantity)
                self.custom_item_window.destroy()
                self.custom_item_window = None
            else:
                print("Invalid custom item details.")
        except (ValueError, TypeError):
            print("Invalid custom item details.")

    def get_discount(self):
        discount_window = tk.Toplevel(self.root)
        discount_window.title("Discount")
        discount_window.geometry("300x100")

        discount_label = tk.Label(discount_window, text="Enter Discount Percentage:")
        discount_label.pack()

        discount_entry = tk.Entry(discount_window, width=10)
        discount_entry.pack()

        apply_discount_button = tk.Button(discount_window, text="Apply Discount", command=lambda: self.apply_discount(discount_entry.get()))
        apply_discount_button.pack()

    def apply_discount(self, discount_percentage):
        try:
            discount_percentage = float(discount_percentage)
            if 0 <= discount_percentage <= 100:
                self.generate_bill(discount_percentage)
            else:
                print("Discount must be between 0 and 100.")
        except ValueError:
            print("Invalid discount value.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryShop(root)
    root.mainloop()
