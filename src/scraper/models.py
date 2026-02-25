from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    title: str
    price: float
    currency: str
    availability: str
    scraped_at: datetime
    url: str