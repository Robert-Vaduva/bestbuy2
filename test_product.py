"""
Unit tests for the Product class using pytest.
"""

import pytest
from products import Product


# ---------- Initialization ----------
def test_init_valid():
    """Verify that a Product is initialized correctly with valid inputs."""
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    assert t_product.get_name() == "Bose QuietComfort Earbuds"
    assert t_product.get_price() == 250.0
    assert t_product.get_quantity() == 500
    assert t_product.is_active() is True


def test_init_invalid():
    """Ensure that Product initialization raises ValueError for invalid inputs."""
    # Empty product name
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product("", price=250, quantity=500)

    # Invalid product price
    with pytest.raises(ValueError, match="Invalid price, please provide a real number,"
                                         " greater than zero"):
        Product("Bose QuietComfort Earbuds", price=-250, quantity=500)
    with pytest.raises(ValueError, match="Invalid price, please provide a real number,"
                                         " greater than zero"):
        Product("Bose QuietComfort Earbuds", price="250a", quantity=500)
    with pytest.raises(ValueError, match="Invalid price, please provide a real number,"
                                         " greater than zero"):
        Product("Bose QuietComfort Earbuds", price="-250a", quantity=500)
    with pytest.raises(ValueError, match="Invalid price, please provide a real number,"
                                         " greater than zero"):
        Product("Bose QuietComfort Earbuds", price="", quantity=500)

    # Invalid product quantity
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        Product("Bose QuietComfort Earbuds", price=250, quantity=-500)
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        Product("Bose QuietComfort Earbuds", price=250, quantity="500a")
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        Product("Bose QuietComfort Earbuds", price=250, quantity="-500a")
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        Product("Bose QuietComfort Earbuds", price=250, quantity="")


# ---------- Quantity Management ----------
def test_get_quantity():
    """Verify that get_quantity returns the current product quantity."""
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    assert t_product.get_quantity() == 500


def test_set_quantity_valid():
    """Ensure set_quantity updates quantity and deactivates product at zero."""
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    t_product.set_quantity(0)
    assert t_product.get_quantity() == 0
    assert t_product.is_active() is False


def test_set_quantity_invalid():
    """Check that set_quantity raises ValueError for invalid quantities."""
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        t_product.set_quantity("")
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        t_product.set_quantity("250a")
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        t_product.set_quantity(-250)


# ---------- Active Status ----------
def test_is_active():
    """Verify is_active reflects product status before and after quantity changes."""
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    assert t_product.is_active() is True
    t_product.set_quantity(0)
    assert t_product.is_active() is False


def test_activate_deactivate():
    """Ensure activate() and deactivate() correctly toggle product active status."""
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    assert t_product.is_active() is True
    t_product.deactivate()
    assert t_product.is_active() is False
    t_product.activate()
    assert t_product.is_active() is True


# ---------- Show ----------
def test_show(capfd):
    """Verify that show() prints the product details in the expected format."""
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    t_product.show()
    captured = capfd.readouterr()
    assert captured.out.strip() == "Bose QuietComfort Earbuds, Price: $250.0, Quantity: 500"


# ---------- Buy ----------
def test_buy_valid():
    """Verify buy() decreases quantity correctly and enforces stock limits."""
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    t_product.buy(251)
    assert t_product.get_quantity() == 249
    with pytest.raises(ValueError, match="The requested quantity is higher than the current stock"):
        t_product.buy(501)


def test_buy_invalid():
    """Ensure buy() raises ValueError for non-numeric or negative quantities."""
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        t_product.buy("")
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        t_product.buy("250a")
    with pytest.raises(ValueError, match="Invalid quantity, please provide a real number,"
                                         " greater or equal to zero"):
        t_product.buy(-250)
