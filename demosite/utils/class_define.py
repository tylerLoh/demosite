""" Utility class definition for design layer

Use Enum object to set symbolic names bound to unique and constant value
"""
from enum import Enum


class ItemType(Enum):
    """
    A class used to define available item type

    Attributes
    ----------
    PRODUCT : int
        product type
    TREATMENT: int
        treatment type
    """

    PRODUCT = 1
    TREATMENT = 2


class DiscountType(Enum):
    """
    A class used to define available discount type symbol

    Attributes
    ----------
    PERCENTAGE: str
        percentage type of discount. eg. 15% = 0.15 discount rate
    DOLLAR: str
        dollar sign type of discount. eg. 25$ = 25$ discount from ori price
    """
    PERCENTAGE = '%'
    DOLLAR = '$'
