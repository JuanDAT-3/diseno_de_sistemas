from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Franja:
    inicio: datetime
    fin: datetime

    def se_solapa(self, otra: "Franja") -> bool:
        return self.inicio < otra.fin and otra.inicio < self.fin

    def __str__(self):
        return f"{self.inicio:%Y-%m-%d %H:%M}-{self.fin:%H:%M}"
