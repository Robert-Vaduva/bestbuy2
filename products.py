"""
Product management module.

Defines the Product class for representing store items with attributes
such as name, price, quantity, and active status. Provides methods for
inventory management, product activation/deactivation, displaying product
details, and processing purchases.
"""

import promotions


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
        self._name = str(name)

        if str(price) == "" or any(elem.isalpha() for elem in str(price)) or float(price) < 0:
            raise ValueError("Invalid price, please provide a real number, "
                             "greater than zero")
        self._price = float(price)

        if (str(quantity) == "" or any(elem.isalpha() for elem in str(quantity))
                or int(quantity) < 0):
            raise ValueError("Invalid quantity, please provide a real number, "
                             "greater or equal to zero")
        self._quantity = int(quantity)
        self._active = active
        if self._quantity == 0:
            self._active = False
        self._promotion = None

    def get_name(self):
        """Return the name of the product."""
        return str(self._name)

    def get_price(self):
        """Return the name of the product."""
        return self._price

    def get_quantity(self):
        """Return the current quantity in stock."""
        return int(self._quantity)

    def set_quantity(self, quantity):
        """Update the product quantity and deactivate if it reaches zero."""
        if (str(quantity) == "" or any(elem.isalpha() for elem in str(quantity))
                or int(quantity) < 0):
            raise ValueError("Invalid quantity, please provide a real number, "
                             "greater or equal to zero")

        self._quantity = int(quantity)
        if self._quantity == 0:
            self._active = False

    def is_active(self):
        """Return True if the product is active, else False."""
        return self._active

    def activate(self):
        """Mark the product as active."""
        self._active = True

    def deactivate(self):
        """Mark the product as inactive."""
        self._active = False

    def show(self):
        """Display product details (name, price, quantity)."""
        promo_info = f", Promotion: {self._promotion.get_name()}" if self._promotion else ""
        return f"{self._name}, Price: ${self._price}, Quantity: {self._quantity}{promo_info}"

    def buy(self, quantity):
        """Reduce stock by given quantity and return total price."""
        if (str(quantity) == "" or any(elem.isalpha() for elem in str(quantity))
                or int(quantity) < 0):
            raise ValueError("Invalid quantity, please provide a real number, "
                             "greater or equal to zero")
        if self._quantity < quantity:
            raise ValueError("The requested quantity is higher than the current stock")

        self.set_quantity(self._quantity - quantity)
        if self._promotion:
            return float(self._promotion.apply_promotion(self, quantity))
        return float(self._price * quantity)

    def set_promotion(self, promotion):
        """Assign a promotion to the product."""
        if isinstance(promotion, promotions.Promotion):
            self._promotion = promotion
        else:
            raise TypeError("Only Promotion instances can be added")

    def remove_promotion(self):
        """Remove the promotion from the product."""
        self._promotion = None

    def get_promotion(self):
        """Return the current promotion of the product."""
        return self._promotion


class NonStockedProduct(Product):
    """
    Represents a product that is never stocked.
    Quantity is always zero, but it can still be 'purchased' for record-keeping or service purposes.
    """

    def __init__(self, name, price):
        """Initialize non-stocked product with zero quantity."""
        super().__init__(name, price, quantity=0)
        self._quantity = 0
        self._active = True

    def set_quantity(self, _quantity):
        """Force quantity to remain zero."""
        self._quantity = 0

    def show(self):
        """Print product name, price, and fixed zero quantity."""
        promo_info = f", Promotion: {self._promotion.get_name()}" if self._promotion else ""
        return f"{self._name}, Price: ${self._price}, Quantity: 0{promo_info}"

    def buy(self, quantity):
        """Reduce stock by given quantity and return total price."""
        if (str(quantity) == "" or any(elem.isalpha() for elem in str(quantity))
                or int(quantity) < 0):
            raise ValueError("Invalid quantity, please provide a real number, "
                             "greater or equal to zero")

        self.set_quantity(self._quantity - quantity) # redundant - used to clear possible failures
        if self._promotion:
            return float(self._promotion.apply_promotion(self, quantity))
        return float(self._price * quantity)


class LimitedProduct(Product):
    """
    Inherits from Product and adds a 'maximum' attribute that restricts
    how many units can be bought in a single order.
    """

    def __init__(self, name, price, quantity, maximum):
        """Initialize product with stock quantity and per-order limit."""
        super().__init__(name, price, quantity)
        self._maximum = maximum

    def get_maximum(self):
        """Return the maximum allowed quantity per order."""
        return self._maximum

    def set_maximum(self, maximum):
        """Set the maximum allowed quantity per order."""
        if (str(maximum) == "" or any(elem.isalpha() for elem in str(maximum))
                or int(maximum) < 0):
            raise ValueError("Invalid maximum quantity, please provide a real number, "
                             "greater than zero")
        self._maximum = int(maximum)

    def show(self):
        """Print product name, price, and fixed zero quantity."""
        promo_info = f", Promotion: {self._promotion.get_name()}" if self._promotion else ""
        return (f"{self._name}, Price: ${self._price}, "
                f"Quantity: {self._quantity}, Limit: {self._maximum}{promo_info}")

    def buy(self, quantity):
        """Purchase quantity if valid and within stock and limit."""
        if (str(quantity) == "" or any(elem.isalpha() for elem in str(quantity))
                or int(quantity) < 0):
            raise ValueError("Invalid quantity, please provide a real number, "
                             "greater than zero")
        if self._quantity < quantity:
            raise ValueError("The requested quantity is higher than the current stock")
        if self._maximum < quantity:
            raise ValueError("The requested quantity is higher than maximum per order")

        self.set_quantity(self._quantity - quantity)
        if self._promotion:
            return float(self._promotion.apply_promotion(self, quantity))
        return float(self._price * quantity)


if __name__ == "__main__":
    # setup initial stock of inventory
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    NonStockedProduct("Windows License", price=125),
                    LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice()
    third_one_free = promotions.ThirdOneFree()
    thirty_percent = promotions.PercentDiscount(30)

    # Check promotions
    print(product_list[0].buy(5))
    product_list[0].set_promotion(second_half_price)
    print(product_list[0].buy(5))
    product_list[0].set_promotion(third_one_free)
    print(product_list[0].buy(5))
    product_list[0].set_promotion(thirty_percent)
    print(product_list[0].buy(5))
    product_list[0].remove_promotion()
    print(product_list[0].buy(5))
