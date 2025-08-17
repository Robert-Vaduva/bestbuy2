"""
This module defines the Promotion abstract base class and its concrete implementations.

Promotions can be attached to products to modify their purchase price based on specific rules.
Each promotion must implement the `apply_promotion(product, quantity)` method, which calculates
the total discounted price for a given product and quantity.

Available promotions:
- SecondHalfPrice: Every second item is sold at half price.
- ThirdOneFree: Every third item is free (buy 2, get 1 free).
- PercentDiscount: Applies a percentage discount to all items.
"""


from abc import ABC, abstractmethod


class Promotion(ABC):
    """Abstract base class for all promotions, requiring a name and an apply_promotion method."""
    def __init__(self, name: str):
        """Initialize promotion with a name."""
        self._name = name

    def get_name(self):
        """Return the promotion name."""
        return self._name

    @abstractmethod
    def apply_promotion(self, product, quantity: int):
        """Apply the promotion to the given product and quantity."""
        ...


class SecondHalfPrice(Promotion):
    """Promotion where every second product is sold at half price."""
    def __init__(self):
        """Initialize 'Second Half Price' promotion."""
        super().__init__(name="Second Half price!")

    def apply_promotion(self, product, quantity):
        """Apply second-half-price discount to the purchase."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        pairs = quantity // 2
        remainder = quantity % 2
        return (pairs * 1.5 + remainder) * product.get_price()


class ThirdOneFree(Promotion):
    """Promotion where every third product is free (buy 2, get 1 free)."""
    def __init__(self):
        """Initialize 'Third One Free' promotion."""
        super().__init__(name="Third One Free!")

    def apply_promotion(self, product, quantity: int) -> float:
        """Apply buy-two-get-one-free discount to the purchase."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        groups_of_three = quantity // 3
        remainder = quantity % 3
        return (groups_of_three * 2 + remainder) * product.get_price()


class PercentDiscount(Promotion):
    """Promotion that applies a percentage discount to all items in the purchase."""
    def __init__(self, disc_percent: float):
        """Initialize percent discount promotion."""
        if (str(disc_percent) == "" or any(elem.isalpha() for elem in str(disc_percent))
                or int(disc_percent) < 0) or int(disc_percent) > 100:
            raise ValueError("Invalid discount provided, please give a number between 0 and 100")

        super().__init__(name=f"{disc_percent}% off!")
        self._percent = disc_percent

    def get_percent(self):
        """Return the discount percentage of the promotion."""
        return self._percent

    def apply_promotion(self, product, quantity: int) -> float:
        """Apply percentage discount to the purchase."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        discount_multiplier = (100 - self._percent) / 100
        return quantity * discount_multiplier * product.get_price()
