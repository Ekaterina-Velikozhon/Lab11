from dataclasses import dataclass
from datetime import datetime

from model.product import Product


@dataclass
class Sale:
    P1: Product
    P2: Product
    giorni_comuni: int

    def __hash__(self):
        return hash((self.P1, self.P2))

    def __str__(self):
        return f"Border: {self.P1} - {self.P2}"