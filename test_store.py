"""
Unit tests for the Store class using pytest.
"""


import pytest
import promotions
from store import Store, make_compact_order_list
from products import Product


# ---------- Initialization ----------
def test_init_valid():
    """Test Store initialization with valid product lists."""
    # initialization with 2 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy = Store([bose, mac])
    assert best_buy.get_list_of_products()[0] == bose
    assert best_buy.get_list_of_products()[0].is_active() is True
    assert best_buy.get_list_of_products()[1] == mac
    assert best_buy.get_list_of_products()[1].is_active() is True

    # initialization with empty list
    best_buy = Store([])
    assert len(best_buy.get_list_of_products()) == 0


def test_init_invalid():
    """Test Store initialization with invalid data types."""
    # initialization with other types than list
    best_buy = Store({0: "0", 1: "1"})
    assert len(best_buy.get_list_of_products()) == 0
    best_buy = Store(((0, 0), (1, 1)))
    assert len(best_buy.get_list_of_products()) == 0
    best_buy = Store(13)
    assert len(best_buy.get_list_of_products()) == 0


# ---------- Quantity Management ----------
def test_add_product_valid():
    """Test adding valid Product instances to the store."""
    # start with an empty store
    best_buy = Store([])
    assert len(best_buy.get_list_of_products()) == 0

    # add one product and check the product list
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    best_buy.add_product(bose)
    assert best_buy.get_list_of_products()[0] == bose
    assert best_buy.get_list_of_products()[0].is_active() is True

    # add another product and check the product list
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy.add_product(mac)
    assert best_buy.get_list_of_products()[1] == mac
    assert best_buy.get_list_of_products()[1].is_active() is True


def test_add_product_invalid():
    """Test adding invalid product types raises TypeError."""
    # start with an empty store
    best_buy = Store([])
    assert len(best_buy.get_list_of_products()) == 0

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
    assert best_buy.get_list_of_products()[0] == bose
    assert best_buy.get_list_of_products()[0].is_active() is True
    assert best_buy.get_list_of_products()[1] == mac
    assert best_buy.get_list_of_products()[1].is_active() is True
    assert len(best_buy.get_list_of_products()) == 2

    # remove 1st product
    best_buy.remove_product(bose)
    assert bose is not best_buy.get_list_of_products()
    assert best_buy.get_list_of_products()[0] == mac
    assert best_buy.get_list_of_products()[0].is_active() is True
    assert len(best_buy.get_list_of_products()) == 1

    # remove 2nd product
    best_buy.remove_product(mac)
    assert mac is not best_buy.get_list_of_products()
    assert len(best_buy.get_list_of_products()) == 0


def test_remove_product_invalid(capfd):
    """Test removing products not present in the store."""
    # initialization with 2 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy = Store([bose, mac])
    assert best_buy.get_list_of_products()[0] == bose
    assert best_buy.get_list_of_products()[0].is_active() is True
    assert best_buy.get_list_of_products()[1] == mac
    assert best_buy.get_list_of_products()[1].is_active() is True
    assert len(best_buy.get_list_of_products()) == 2

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


def test_order_promotions():
    """Test placing valid orders and updating quantities."""
    # initialization with 3 products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    google = Product("Google Pixel 7", price=500, quantity=250)
    best_buy = Store([bose, mac, google])

    # check order in case of same products added multiple times
    second_half_price = promotions.SecondHalfPrice()
    bose.set_promotion(second_half_price)
    price = best_buy.order([(bose, 1), (bose, 1)])
    assert price == bose.get_price() * 1.5

    # check order in case of same products added multiple times
    third_one_free = promotions.ThirdOneFree()
    google.set_promotion(third_one_free)
    price = best_buy.order([(google, 1), (google, 2)])
    assert price == google.get_price() * 2.0

    # check order in case of same products added multiple times
    thirty_percent = promotions.PercentDiscount(disc_percent=30)
    mac.set_promotion(thirty_percent)
    price = best_buy.order([(mac, 1), (mac, 2)])
    assert round(price, 1) == 3 * mac.get_price() * 0.7


# ---------- Compact List ----------
def test_make_compact_order_list_valid():
    """Verify that it correctly sums quantities for duplicates and handles various inputs."""
    # check list with duplicate elements
    check_list = [("a", 5), ("b", 3), ("a", 7), ("c", 2)]
    assert make_compact_order_list(check_list) == [('a', 12), ('b', 3), ('c', 2)]

    # check empty list
    check_list = []
    assert make_compact_order_list(check_list) == []

    # check list with unique elements
    check_list = [("a", 5), ("b", 3), ("c", 7), ("d", 2)]
    assert make_compact_order_list(check_list) == [("a", 5), ("b", 3), ("c", 7), ("d", 2)]


def test_make_compact_order_list_invalid(capfd):
    """Ensure make_compact_order_list returns [] and prints an error for invalid input types."""
    # check with a number instead of a list
    check_list = 12
    assert make_compact_order_list(check_list) == []
    captured = capfd.readouterr()
    assert captured.out.strip() == "Please provide a list of tuples of type (product, quantity)"

    # check with a dictionary instead of a list
    check_list = {("a", 5), ("b", 3), ("c", 7), ("d", 2)}
    assert make_compact_order_list(check_list) == []
    captured = capfd.readouterr()
    assert captured.out.strip() == "Please provide a list of tuples of type (product, quantity)"
