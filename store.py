"""
Store inventory management.

Provides the Store class for adding, removing, and listing products,
as well as tracking inventory.
"""


import products


class Store:
    """Store that holds and manages multiple products."""
    def __init__(self, list_of_products=None):
        """Initialize store with a list of products."""
        self._list_of_products = []
        if isinstance(list_of_products, list) and list_of_products is not None:
            for prod in list_of_products:
                prod.activate()
                self.add_product(prod)

    def add_product(self, prod):
        """Add a Product to the store."""
        if isinstance(prod, products.Product):
            self._list_of_products.append(prod)
        else:
            raise TypeError("Only Product instances can be added to the store")

    def remove_product(self, prod):
        """Remove a Product from the store."""
        try:
            self._list_of_products.remove(prod)
        except ValueError:
            print("Product not found in inventory")

    def get_total_quantity(self):
        """Return the total number of products."""
        total_quantity = 0
        for prod in self._list_of_products:
            total_quantity += prod.get_quantity()
        return int(total_quantity)

    def get_all_products(self):
        """Return a list of active products."""
        active_products = []
        for prod in self._list_of_products:
            if prod.is_active():
                active_products.append(prod)
        return active_products

    def get_list_of_products(self):
        """Return the store's list of products."""
        return self._list_of_products

    def order(self, shopping_list):
        """ Process a list of (Product, quantity) purchases and return total cost."""
        total_price = 0
        for prod, quantity in shopping_list:
            if prod in self._list_of_products:
                total_price += prod.buy(quantity)
                if prod.get_quantity() == 0:
                    self.remove_product(prod)
        return total_price
