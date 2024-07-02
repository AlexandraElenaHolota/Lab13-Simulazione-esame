from dataclasses import dataclass
@dataclass
class State:
    id: str
    Lat: float
    Lng: float

    def __str__(self):
        return f"{self.id} {self.Lat} {self.Lng}"

    def __hash__(self):
        return hash(self.id)
