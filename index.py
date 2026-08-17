# Tkinter Imports
import tkinter as tk
from tkinter import ttk

# Dictionaries storing the Items on the menu and their prices
pizza_choices = {
    "--Select Pizza Type--": 0.00,
    "Margherita": 1.00,
    "Pepperoni": 1.20,
    "Ham": 1.30,
    "Meat Feast": 1.50}
topping_choices = {
    "Extra Cheese": 0.80,
    "Ham": 0.30,
    "Pepperoni": 0.60,
    "Chicken": 0.50}
side_choices = {
    "Fries": 1.60,
    "Salad": 1.40,
    "Apple Slices": 0.80,
    "Potato Wedges": 1.80,
    "Halloumi Fries": 2.00}
cart = []

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    # Abstraction Method to get item details, to be overridden by child classes
    def get_details(self):
        return f"{self.name}: £{self.price:.2f}"

class Pizza(Item): # Pizza Class
    def __init__(self, pizza_type, size, toppings):
        base_price = pizza_choices.get(pizza_type, 0)
        pizza_price = base_price * size
        self.size = size
        # Topping Variables
        self.selected_toppings = toppings
        topping_total = sum(topping_choices[t] for t in toppings)
        # Inheriting from parent Item Class
        super().__init__(pizza_type, pizza_price + topping_total)
    # Polymorphism Method to get pizza details
    def get_details(self):
        toppings_str = ", ".join(self.selected_toppings) if self.selected_toppings else "None"
        return f"Pizza: {self.name}\n Pizza Size: {self.size} inches \nExtra Toppings: {toppings_str}\nTotal Pizza Price: £{self.price:.2f}"

# Side Order Class
class SideOrder(Item):
    def __init__(self, side_name, quantity):
        self.quantity = quantity
        total_side_price = side_choices[side_name] * quantity
        # Inheriting from parent Item Class
        super().__init__(side_name, total_side_price)
    # Polymorphism Method to get side item details
    def get_details(self):
        return f"{self.name} (x{self.quantity}): £{self.price:.2f}"

# Side Order GUI
class SideOrderGUI:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.geometry("500x400")
        self.window.title("Side Orders")
        self.window.configure(bg="#eed9c4")
        tk.Label(self.window, text="Side Orders Selection", font=("Arial", 14, "bold"), bg="#fca503", fg="white", relief="raised", width=52, height=2).pack()
        self.selected_sides = {}

        for side in side_choices:
            tk.Label(self.window, text=side, bg="#eed9c4").pack()
            quantity = tk.Spinbox(self.window, from_=0, to=50, width=3)
            quantity.pack(pady=2)
            self.selected_sides[side] = quantity
        ttk.Separator(self.window, orient='horizontal').pack(fill='x', pady=10)
        tk.Button(self.window, text="Add to Order", width=35, command=self.validate).pack()

    # Checks for selected sides and adds them to the cart
    def validate(self):
        for name, quantity in self.selected_sides.items():
            quantity = int(quantity.get())
            if quantity > 0:
                cart.append(SideOrder(name, quantity))
        self.window.destroy()

# Order Summary GUI Clasas
class OrderSummaryGUI:
    def __init__(self, root):
        # GUI Set Up
        self.order_summary = tk.Toplevel(root)
        self.order_summary.geometry("500x400")
        self.order_summary.title("Order Summary")
        self.open_order_summary()
    # Creates the order summary widgets
    def open_order_summary(self):
        tk.Label(self.order_summary, text="Order Summary").pack()
        tk.Label(self.order_summary, text="-----------------------------------").pack()
        cart_total = 0 # Stores the total cost
        # Iterates through the cart and displays the details of each item, while calculating the total cost
        for item in cart:
            tk.Label(self.order_summary, text=item.get_details()).pack()
            cart_total += item.price
            tk.Label(self.order_summary, text="-----------------------------------").pack()
        tk.Label(self.order_summary, text=f"Total Cost: £{cart_total:.2f}").pack()

class PizzaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Way Pizza Parlour")
        self.root.geometry("500x480")
        self.root.configure(bg="#eed9c4")
        # Checks if window exists to prevent duplicates
        self.side_menu_instance = None
        self.order_summary_instance = None
        # Storing user input
        self.var_pizza_type = tk.StringVar()
        self.var_pizza_size = tk.IntVar(value = 10)
        self.topping_selection = {}
        # Widget and menu display
        self.create_widgets()
        self.menu_creation()

    def menu_creation(self):
        main_menu = tk.Menu(self.root)
        self.root.config(menu=main_menu)
        # Pizza Menu Cascade
        pizzas_menu = tk.Menu(main_menu, tearoff=0)
        pizzas_menu.add_command(label="Pizza Menu and Customisation")
        main_menu.add_cascade(label="Pizzas", menu=pizzas_menu)
        # Side Orders Cascade
        sides_menu = tk.Menu(main_menu, tearoff=0)
        sides_menu.add_command(label="Open Sides Window", command=self.open_side_menu)
        main_menu.add_cascade(label="Side Orders", menu=sides_menu)
        # Order Summary Cascade
        summary_menu = tk.Menu(main_menu, tearoff=0)
        summary_menu.add_command(label="View Receipt", command=self.open_order_summary)
        main_menu.add_cascade(label="Order Summary", menu=summary_menu)
        self.root.config(menu=main_menu)

    def create_widgets(self):
        # Pizza Type input field
        tk.Label(self.root, text="Pizza Type", bg="#fca503", fg="white", font=("Arial", 14, "bold"), relief=tk.RAISED, width=52, bd=2, height=2).pack()
        self.pizza_type_inp = ttk.Combobox(self.root, values=list(pizza_choices.keys()), state="readonly")
        self.pizza_type_inp.pack(pady=10)
        self.pizza_type_inp.set("--Select Pizza Type--")
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=10)

        # Pizza size input field
        tk.Label(self.root, text="Pizza Size", bg="#fca503", fg="white", font=("Arial", 14, "bold"), relief=tk.RAISED, width=52, bd=2, height=2).pack()
        tk.Label(self.root, text="Input what size you would like your pizza in inches", bg="#eed9c4").pack(pady=5)
        self.pizza_size_inp = tk.Spinbox(self.root, from_=8, to=18, width=2, state="readonly")
        self.pizza_size_inp.pack()
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=10)

        # Extra Toppings selection using checkboxes
        tk.Label(self.root, text="Extra Toppings", bg="#fca503", fg="white", font=("Arial", 14, "bold"), relief=tk.RAISED, width=52, bd=2, height=2).pack()
        for topping in topping_choices:
            selected = tk.BooleanVar()
            topping_checkbox = tk.Checkbutton(self.root, text=f"{topping}: £{topping_choices[topping]:.2f}", bg="#eed9c4", variable = selected).pack()
            self.topping_selection[topping] = selected
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=10)
        tk.Button(self.root, text = "Add to Order", bg="grey", width=30, command=self.add_to_cart).pack()

    # Function that validates user input and appends the pizza object to the cart if valid
    def add_to_cart(self):
        try:
            pizza_type = self.pizza_type_inp.get()
            # Checks if the label is already present if so it is destroyed to avoid multiple error message display
            if hasattr(self, 'error_label'):
                self.error_label.destroy()
            # Checks if the pizza type isn't the default value if not it pizza object is created and added to the cart
            if pizza_type == "--Select Pizza Type--":
                self.error_label = tk.Label(self.root, text="Please select a pizza type.", fg="red", bg="#eed9c4")
                self.error_label.pack()
            else:
                self.pizza_type_inp.set("--Select Pizza Type--")
                pizza_size = int(self.pizza_size_inp.get())
                selected_toppings = [t for t, topping in self.topping_selection.items() if topping.get()]
                pizza_object = Pizza(pizza_type, pizza_size, selected_toppings)
                cart.append(pizza_object)
        except ValueError:
            tk.label(self.root, text = "Error: Input Error", fg="red", bg="#eed9c4")

    # Opens the side order menu on click if window instance doesn't exist
    def open_side_menu(self):
        if self.side_menu_instance is not None and self.side_menu_instance.window.winfo_exists():
            self.side_menu_instance.window.lift() # Brings existing window to front
            self.side_menu_instance.window.focus_force()
        else:
            self.side_menu_instance = SideOrderGUI(self.root)

    # Opens the order summary menu on click if window instance doesn't exist
    def open_order_summary(self):
        if self.order_summary_instance is not None and self.order_summary_instance.order_summary.winfo_exists():
            self.order_summary_instance.order_summary.lift() # Brings existing window to front
            self.order_summary_instance.order_summary.focus_force()
        else:
            self.order_summary_instance = OrderSummaryGUI(self.root)

# Main global Function to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    my_app = PizzaGUI(root)
    root.mainloop()