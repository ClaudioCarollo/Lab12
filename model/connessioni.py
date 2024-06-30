from dataclasses import dataclass

from model.retailer import Retailer


@dataclass
class Connessione:
    retailer1: Retailer
    retailer2: Retailer
    peso: int