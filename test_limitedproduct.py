"""
Unit tests for the LimitedProduct class.

These tests verify that a LimitedProduct:
- Initializes correctly with name, price, quantity, and maximum per-order limit.
- Accurately returns and updates the maximum purchase limit.
- Rejects invalid maximum values such as empty strings, non-numeric input, or negatives.
- Processes valid purchases within stock and limit, updating quantity accordingly.
- Raises appropriate errors when purchase quantity is invalid,
  exceeds stock, or exceeds the per-order limit.

Tests are written using pytest and assume LimitedProduct inherits from Product.
"""


import pytest
from products import LimitedProduct


# ---------- Initialization ----------
def test_init():
    """Test initialization of LimitedProduct with all attributes."""
    t_product = LimitedProduct("Bose QuietComfort Earbuds", price=250, quantity=100, maximum=5)
    assert t_product.get_name() == "Bose QuietComfort Earbuds"
    assert t_product.get_price() == 250.0
    assert t_product.get_quantity() == 100
    assert t_product.is_active() is True
    assert t_product.get_maximum() == 5


# ---------- Maximum ----------
def test_get_maximum():
    """Test retrieving the maximum purchase limit."""
    t_product = LimitedProduct("Bose QuietComfort Earbuds", price=250, quantity=100, maximum=50)
    assert t_product.get_maximum() == 50
    t_product = LimitedProduct("MacBook Air M2", price=1450, quantity=100, maximum=69)
    assert t_product.get_maximum() == 69


def test_set_maximum_valid():
    """Test setting a valid maximum purchase limit."""
    t_product = LimitedProduct("Bose QuietComfort Earbuds", price=250, quantity=100, maximum=50)
    assert t_product.get_maximum() == 50
    t_product.set_maximum(69)
    assert t_product.get_maximum() == 69


def test_set_maximum_invalid():
    """Test setting an invalid maximum purchase limit raises ValueError."""
    t_product = LimitedProduct("Bose QuietComfort Earbuds", price=250, quantity=100, maximum=50)
    assert t_product.get_maximum() == 50

    with pytest.raises(ValueError, match="Invalid maximum quantity, please provide a real number, "
                                         "greater than zero"):
        t_product.set_maximum("")
    with pytest.raises(ValueError, match="Invalid maximum quantity, please provide a real number, "
                                         "greater than zero"):
        t_product.set_maximum("150a")
    with pytest.raises(ValueError, match="Invalid maximum quantity, please provide a real number, "
                                         "greater than zero"):
        t_product.set_maximum(-231)


# ---------- Buy ----------
def test_buy_valid():
    """Test buying valid quantities within stock and limit."""
    t_product = LimitedProduct("MacBook Air M2", price=1450, quantity=100, maximum=15)
    assert t_product.buy(10) == 14500
    assert t_product.get_quantity() == 90

    assert t_product.buy(14) == 20300
    assert t_product.get_quantity() == 76


def test_buy_invalid(capfd):
    """Test buying invalid quantities or exceeding stock/limit raises ValueError."""
    # check invalid order
    t_product = LimitedProduct("MacBook Air M2", price=1450, quantity=100, maximum=15)
    t_product.buy("")
    captured = capfd.readouterr()
    assert captured.out.strip() == ("Invalid quantity, please provide a real number,"
                                    " greater or equal to zero")

    t_product.buy("250a")
    captured = capfd.readouterr()
    assert captured.out.strip() == ("Invalid quantity, please provide a real number,"
                                    " greater or equal to zero")

    t_product.buy(-250)
    captured = capfd.readouterr()
    assert captured.out.strip() == ("Invalid quantity, please provide a real number,"
                                    " greater or equal to zero")

    # check order greater than quantity and lower than maximum
    t_product = LimitedProduct("MacBook Air M2", price=1450, quantity=10, maximum=15)
    t_product.buy(14)
    captured = capfd.readouterr()
    assert captured.out.strip() == "The requested quantity is higher than the current stock"

    # check order greater than maximum
    t_product = LimitedProduct("MacBook Air M2", price=1450, quantity=20, maximum=15)
    t_product.buy(16)
    captured = capfd.readouterr()
    assert captured.out.strip() == "The requested quantity is higher than maximum per order"
