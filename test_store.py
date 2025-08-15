"""
Unit tests for the Store class using pytest.
"""

import pytest
from store import Store
from products import Product


# ---------- Initialization ----------
def test_init_valid():
    """Test Store initialization with valid product lists."""
    # initialization with 2 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy = Store([bose, mac])
    assert best_buy.list_of_products[0] == bose
    assert best_buy.list_of_products[0].is_active() is True
    assert best_buy.list_of_products[1] == mac
    assert best_buy.list_of_products[1].is_active() is True

    # initialization with empty list
    best_buy = Store([])
    assert len(best_buy.list_of_products) == 0


def test_init_invalid():
    """Test Store initialization with invalid data types."""
    # initialization with other types than list
    best_buy = Store({0: "0", 1: "1"})
    assert len(best_buy.list_of_products) == 0
    best_buy = Store(((0, 0), (1, 1)))
    assert len(best_buy.list_of_products) == 0
    best_buy = Store(13)
    assert len(best_buy.list_of_products) == 0


# ---------- Quantity Management ----------
def test_add_product_valid():
    """Test adding valid Product instances to the store."""
    # start with an empty store
    best_buy = Store([])
    assert len(best_buy.list_of_products) == 0

    # add one product and check the product list
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    best_buy.add_product(bose)
    assert best_buy.list_of_products[0] == bose
    assert best_buy.list_of_products[0].is_active() is True

    # add another product and check the product list
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy.add_product(mac)
    assert best_buy.list_of_products[1] == mac
    assert best_buy.list_of_products[1].is_active() is True


def test_add_product_invalid():
    """Test adding invalid product types raises TypeError."""
    # start with an empty store
    best_buy = Store([])
    assert len(best_buy.list_of_products) == 0

    # add one product and check the product list
    with pytest.raises(TypeError, match="Only Product instances can be added to the store"):
        best_buy.add_product({0: "0", 1: "1"})
    with pytest.raises(TypeError, match="Only Product instances can be added to the store"):
        best_buy.add_product(((0, 0), (1, 1)))
    with pytest.raises(TypeError, match="Only Product instances can be added to the store"):
        best_buy.add_product(13)


def test_remove_product_valid():
    """Test removing existing products from the store."""
    # initialization with 2 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy = Store([bose, mac])
    assert best_buy.list_of_products[0] == bose
    assert best_buy.list_of_products[0].is_active() is True
    assert best_buy.list_of_products[1] == mac
    assert best_buy.list_of_products[1].is_active() is True
    assert len(best_buy.list_of_products) == 2

    # remove 1st product
    best_buy.remove_product(bose)
    assert bose is not best_buy.list_of_products
    assert best_buy.list_of_products[0] == mac
    assert best_buy.list_of_products[0].is_active() is True
    assert len(best_buy.list_of_products) == 1

    # remove 2nd product
    best_buy.remove_product(mac)
    assert mac is not best_buy.list_of_products
    assert len(best_buy.list_of_products) == 0


def test_remove_product_invalid(capfd):
    """Test removing products not present in the store."""
    # initialization with 2 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy = Store([bose, mac])
    assert best_buy.list_of_products[0] == bose
    assert best_buy.list_of_products[0].is_active() is True
    assert best_buy.list_of_products[1] == mac
    assert best_buy.list_of_products[1].is_active() is True
    assert len(best_buy.list_of_products) == 2

    # try to remove products not present in list
    google = Product("Google Pixel 7", price=500, quantity=250)
    best_buy.remove_product(google)
    captured = capfd.readouterr()
    assert captured.out.strip() == "Product not found in inventory"

    best_buy.remove_product({0: "0", 1: "1"})
    captured = capfd.readouterr()
    assert captured.out.strip() == "Product not found in inventory"

    best_buy.remove_product(((0, 0), (1, 1)))
    captured = capfd.readouterr()
    assert captured.out.strip() == "Product not found in inventory"

    best_buy.remove_product(13)
    captured = capfd.readouterr()
    assert captured.out.strip() == "Product not found in inventory"

# ---------- Inventory ----------
def test_get_total_quantity():
    """Test calculating the total quantity of products."""
    # initialization with 2 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy = Store([bose, mac])
    assert best_buy.get_total_quantity() == 600

    # add another product
    google = Product("Google Pixel 7", price=500, quantity=250)
    best_buy.add_product(google)
    assert best_buy.get_total_quantity() == 850

    # remove products
    best_buy.remove_product(bose)
    assert best_buy.get_total_quantity() == 350
    best_buy.remove_product(mac)
    assert best_buy.get_total_quantity() == 250


def test_get_all_products():
    """Test retrieving all products currently in store."""
    # initialization with 2 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy = Store([bose, mac])
    assert best_buy.get_all_products() == [bose, mac]

    # remove products
    best_buy.remove_product(bose)
    assert best_buy.get_all_products() == [mac]

    # add another product
    google = Product("Google Pixel 7", price=500, quantity=250)
    best_buy.add_product(google)
    assert best_buy.get_all_products() == [mac, google]


# ---------- Order ----------
def test_order_valid():
    """Test placing valid orders and updating quantities."""
    # initialization with 3 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    google = Product("Google Pixel 7", price=500, quantity=250)
    best_buy = Store([bose, mac, google])

    # order some products
    assert best_buy.get_total_quantity() == 850
    price = best_buy.order([(bose, 5), (mac, 30), (google, 10)])
    assert price == 49750.0
    assert best_buy.get_total_quantity() == 805


def test_order_invalid():
    """Test placing invalid orders returns correct results."""
    # initialization with 3 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy = Store([bose, mac])

    # check order with empty list
    assert best_buy.get_total_quantity() == 600
    assert best_buy.get_all_products() == [bose, mac]
    assert best_buy.order([]) == 0

    # check order with missing product
    google = Product("Google Pixel 7", price=500, quantity=250)
    price = best_buy.order([(bose, 5), (google, 10)])
    assert best_buy.get_total_quantity() == 595
    assert best_buy.get_all_products() == [bose, mac]
    assert price == 1250
