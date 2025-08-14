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
        self.list_of_products = []
        if isinstance(list_of_products, list) and list_of_products is not None:
            for prod in list_of_products:
                prod.activate()
                self.add_product(prod)

    def add_product(self, prod):
        """Add a Product to the store."""
        if isinstance(prod, products.Product):
            self.list_of_products.append(prod)
        else:
            raise TypeError("Only Product instances can be added to the store")

    def remove_product(self, prod):
        """Remove a Product from the store."""
        try:
            self.list_of_products.remove(prod)
        except ValueError:
            print("Product not found in inventory")

    def get_total_quantity(self):
        """Return the total number of products."""
        total_quantity = 0
        for prod in self.list_of_products:
            total_quantity += prod.quantity
        return int(total_quantity)

    def get_all_products(self):
        """Return a list of active products."""
        active_products = []
        for prod in self.list_of_products:
            if prod.is_active():
                active_products.append(prod)
        return active_products

    def order(self, shopping_list):
        """ Process a list of (Product, quantity) purchases and return total cost."""
        total_price = 0
        for prod, quantity in shopping_list:
            if prod in self.list_of_products:
                total_price += prod.buy(quantity)
                if prod.get_quantity() == 0:
                    self.remove_product(prod)
        return total_price


if __name__ == "__main__":
    bose = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = products.Product("MacBook Air M2", price=1450, quantity=100)

    # instance of a store
    best_buy = Store([bose, mac])
    Store()
    Store({0: "0", 1: "1"})
    Store(((0, 0), (1, 1)))
    print(best_buy.list_of_products)

    pixel = products.Product("Google Pixel 7", price=500, quantity=250)
    best_buy.add_product(pixel)
    best_buy.remove_product("google")

    price = best_buy.order([(bose, 5), (mac, 30), (bose, 10)])
    print(f"Order cost: {price} dollars.")

    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    ]

    best_buy = Store(product_list)
    products = best_buy.get_all_products()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(products[0], 2), (products[1], 2)]))
