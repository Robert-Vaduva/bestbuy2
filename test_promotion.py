"""
Unit tests for promotion classes in the promotions module.

This test suite verifies the correct behavior of all promotion types:
- SecondHalfPrice: ensures every second product is half-price.
- ThirdOneFree: ensures every third product is free.
- PercentDiscount: ensures a percentage discount is correctly applied.

The tests cover:
- Proper initialization of promotions with correct attributes.
- Correct price calculation when promotions are applied with valid quantities.
- Error handling when invalid quantities or invalid promotion parameters are provided.
- Validation of getter methods (e.g., discount percentage).
"""


import pytest
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount
from products import Product


# SecondHalfPrice --------------------
# ---------- Initialization ----------
def test_shp_init():
    """Test SecondHalfPrice initializes with the correct name."""
    t_promotion = SecondHalfPrice()
    assert t_promotion.get_name() == "Second Half price!"


# ---------- Apply promotion ----------
def test_shp_apply_promotion_valid():
    """Test SecondHalfPrice applies correctly for valid quantities."""
    t_promotion = SecondHalfPrice()
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    assert t_promotion.apply_promotion(t_product, 15) == 2875.0


def test_shp_apply_promotion_invalid():
    """Test SecondHalfPrice raises ValueError for invalid quantities."""
    t_promotion = SecondHalfPrice()
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        t_promotion.apply_promotion(t_product, -5)

    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        t_promotion.apply_promotion(t_product, 0)


# ThirdOneFree -----------------------
# ---------- Initialization ----------
def test_tof_init():
    """Test ThirdOneFree initializes with the correct name."""
    t_promotion = ThirdOneFree()
    assert t_promotion.get_name() == "Third One Free!"


# ---------- Apply promotion ----------
def test_tof_apply_promotion_valid():
    """Test ThirdOneFree applies correctly for valid quantities."""
    t_promotion = ThirdOneFree()
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    assert t_promotion.apply_promotion(t_product, 15) == 2500.0


def test_tof_apply_promotion_invalid():
    """Test ThirdOneFree raises ValueError for invalid quantities."""
    t_promotion = ThirdOneFree()
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        t_promotion.apply_promotion(t_product, -5)

    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        t_promotion.apply_promotion(t_product, 0)


# PercentDiscount --------------------
# ---------- Initialization ----------
def test_pd_init_valid():
    """Test PercentDiscount initializes with valid percentages."""
    t_promotion = PercentDiscount(30)
    assert t_promotion.get_name() == "30% off!"
    assert t_promotion.get_percent() == 30

    t_promotion = PercentDiscount(69)
    assert t_promotion.get_name() == "69% off!"
    assert t_promotion.get_percent() == 69


def test_pd_init_invalid():
    """Test PercentDiscount raises ValueError for invalid percentages."""
    with pytest.raises(ValueError, match="Invalid discount provided, "
                                         "please give a number between 0 and 100"):
        PercentDiscount(-1)
    with pytest.raises(ValueError, match="Invalid discount provided, "
                                         "please give a number between 0 and 100"):
        PercentDiscount(101)
    with pytest.raises(ValueError, match="Invalid discount provided, "
                                         "please give a number between 0 and 100"):
        PercentDiscount("")
    with pytest.raises(ValueError, match="Invalid discount provided, "
                                         "please give a number between 0 and 100"):
        PercentDiscount("50a")

# ---------- Get percent ----------
def test_pd_get_percent():
    """Test PercentDiscount returns the correct percentage."""
    t_promotion = PercentDiscount(69)
    assert t_promotion.get_percent() == 69

    t_promotion = PercentDiscount(99)
    assert t_promotion.get_percent() == 99

    t_promotion = PercentDiscount(42)
    assert t_promotion.get_percent() == 42


# ---------- Apply promotion ----------
def test_pd_apply_promotion_valid():
    """Test PercentDiscount applies correctly for valid quantities."""
    t_promotion = PercentDiscount(42)
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    assert t_promotion.apply_promotion(t_product, 15) == 2175.0


def test_pd_apply_promotion_invalid():
    """Test PercentDiscount raises ValueError for invalid quantities."""
    t_promotion = PercentDiscount(42)
    t_product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        t_promotion.apply_promotion(t_product, -5)

    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        t_promotion.apply_promotion(t_product, 0)
