"""
Unit tests for the NonStockedProduct class.

These tests validate that a NonStockedProduct:
- Initializes correctly with a name, price, and zero quantity.
- Ignores any attempt to set its quantity (always remains zero).
- Displays its details correctly through the show() method.
- Correctly processes purchases without altering its stock level.
- Raises ValueError when attempting to buy with invalid quantities.

Tests are written using pytest and assume that the NonStockedProduct
class inherits from the Product base class.
"""


import pytest
from products import NonStockedProduct


# ---------- Initialization ----------
def test_init():
    """Test initialization of NonStockedProduct with name and price."""
    t_product = NonStockedProduct("Bose QuietComfort Earbuds", price=250)
    assert t_product.get_name() == "Bose QuietComfort Earbuds"
    assert t_product.get_price() == 250.0
    assert t_product.get_quantity() == 0
    assert t_product.is_active() is True


# ---------- Quantity Management ----------
def test_set_quantity():
    """Test that set_quantity always keeps quantity at zero."""
    t_product = NonStockedProduct("Bose QuietComfort Earbuds", price=250)
    t_product.set_quantity(321)
    assert t_product.get_name() == "Bose QuietComfort Earbuds"
    assert t_product.get_price() == 250.0
    assert t_product.get_quantity() == 0
    assert t_product.is_active() is True

    t_product.set_quantity(123)
    assert t_product.get_name() == "Bose QuietComfort Earbuds"
    assert t_product.get_price() == 250.0
    assert t_product.get_quantity() == 0
    assert t_product.is_active() is True


# ---------- Show ----------
def test_show():
    """Test that show prints correct product details."""
    bose = NonStockedProduct("Bose QuietComfort Earbuds", price=250)
    assert bose.show() == "Bose QuietComfort Earbuds, Price: $250.0, Quantity: 0"

    mac = NonStockedProduct("MacBook Air M2", price=1450)
    assert mac.show() == "MacBook Air M2, Price: $1450.0, Quantity: 0"


# ---------- Buy ----------
def test_buy_valid():
    """Test buying valid quantities returns correct total price."""
    t_product = NonStockedProduct("Bose QuietComfort Earbuds", price=250)
    assert t_product.buy(10) == 2500
    assert t_product.get_quantity() == 0
    assert t_product.buy(50) == 12500
    assert t_product.get_quantity() == 0


def test_buy_invalid():
    """Test buying invalid quantities raises ValueError."""
    t_product = NonStockedProduct("Bose QuietComfort Earbuds", price=250)
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        t_product.buy("")
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        t_product.buy("250a")
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        t_product.buy(-250)
