"""
Main application for interacting with the store.

Provides a text-based menu to list products, show inventory totals,
place orders, and exit the application.
"""
import sys
import products
import store


def list_all_products(store_p):
    """Print all active products with their price and quantity."""
    print("------")
    index = 1
    for prod in store_p.get_all_products():
        print(f"{index}. {prod.name}, Price: ${prod.price}, Quantity: {prod.quantity}")
        index += 1
    print("------")


def show_total_amount(store_p):
    """Display the total number of products in the store."""
    print(f"Total of {store_p.get_total_quantity()} items in store")


def make_an_order(store_p):
    """Prompt user to create an order and process it."""
    list_all_products(store_p)
    print("When you want to finish order, enter empty text.")
    order_list = []
    while True:
        try:
            product_nr = input("Which product number do you want (e.g. 1?)")
            if not product_nr:
                break
            if (any(elem.isalpha() for elem in str(product_nr)) or int(product_nr) == 0 or
                    int(product_nr) > len(store_p.list_of_products)):
                print("Error adding product!\n")
                continue
            quantity = int(input("What amount do you want? "))
            if not quantity:
                break
            if (any(elem.isalpha() for elem in str(quantity)) or
                    int(quantity) > store_p.list_of_products[int(product_nr) - 1].get_quantity()):
                print("Error while making order! Quantity larger than what exists\n")
                continue

            order_list.append((store_p.list_of_products[int(product_nr) - 1], quantity))
            print("Product added to list!\n")
        except (ValueError, TypeError) as error:
            print(error)
    total_payment = store_p.order(order_list)
    if total_payment > 0:
        print("********")
        print(f"Order made! Total payment {total_payment}")


def exit_fnc(_store_p):
    """Exit the application with a goodbye message."""
    sys.exit()


FUNCTIONS = {1: list_all_products, 2: show_total_amount,
             3: make_an_order, 4: exit_fnc}


def start(store_p):
    """Run the store menu loop until the user quits."""
    while True:
        try:
            print()
            print("   Store Menu")
            print("   ----------")
            print("1. List all products in store")
            print("2. Show total amount in store")
            print("3. Make an order")
            print("4. Quit")
            user_input = int(input("Please choose a number: "))
            if 0 < user_input <= len(FUNCTIONS):
                FUNCTIONS[user_input](store_p)
        except (ValueError, TypeError):
            print("Error with your choice! Try again!")


if __name__ == "__main__":
    # setup initial stock of inventory
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250)
                    ]
    best_buy = store.Store(product_list)
    start(best_buy)
