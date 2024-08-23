
class Ponto:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def print(self) -> None:
        print("Ponto (", self.x, ",", self.y, ")")

    def set(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Ponto(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Ponto(x, y)

    def __mul__(self, escalar: float):
        x = self.x * escalar
        y = self.y * escalar
        return Ponto(x, y)
