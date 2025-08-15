"""
Product management module.

Defines the Product class for representing store items with attributes
such as name, price, quantity, and active status. Provides methods for
inventory management, product activation/deactivation, displaying product
details, and processing purchases.
"""


class Product:
    """
    Represents a product with a name, price, quantity, and active status.
    Provides methods to manage inventory, update status, display details,
    and process purchases.
    """
    def __init__(self, name, price, quantity, active=True):
        """Initialize a product with name, price, and quantity."""
        if str(name) == "":
            raise ValueError("Product name cannot be empty")
        self.name = str(name)

        if str(price) == "" or any(elem.isalpha() for elem in str(price)) or float(price) < 0:
            raise ValueError("Invalid price, please provide a real number, "
                             "greater than zero")
        self.price = float(price)

        if (str(quantity) == "" or any(elem.isalpha() for elem in str(quantity))
                or int(quantity) < 0):
            raise ValueError("Invalid quantity, please provide a real number, "
                             "greater or equal to zero")
        self.quantity = int(quantity)
        self.active = active
        if self.quantity == 0:
            self.active = False

    def get_quantity(self):
        """Return the current quantity in stock."""
        return int(self.quantity)

    def set_quantity(self, quantity):
        """Update the product quantity and deactivate if it reaches zero."""
        if (str(quantity) == "" or any(elem.isalpha() for elem in str(quantity))
                or int(quantity) < 0):
            raise ValueError("Invalid quantity, please provide a real number, "
                             "greater or equal to zero")

        self.quantity = int(quantity)
        if self.quantity == 0:
            self.active = False

    def is_active(self):
        """Return True if the product is active, else False."""
        return self.active

    def activate(self):
        """Mark the product as active."""
        self.active = True

    def deactivate(self):
        """Mark the product as inactive."""
        self.active = False

    def show(self):
        """Display product details (name, price, quantity)."""
        print(f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}")

    def buy(self, quantity):
        """Reduce stock by given quantity and return total price."""
        if (str(quantity) == "" or any(elem.isalpha() for elem in str(quantity))
                or int(quantity) < 0):
            raise ValueError("Invalid quantity, please provide a real number, "
                             "greater or equal to zero")
        if self.quantity < quantity:
            raise ValueError("The requested quantity is higher than the current stock")

        self.set_quantity(self.quantity-quantity)
        return float(self.price * quantity)
