from enum import Enum


class ItemType(Enum):
    PRODUCT = 1
    TREATMENT = 2


class DiscountType(Enum):
    PERCENTAGE = '%'
    DOLLAR = '$'
