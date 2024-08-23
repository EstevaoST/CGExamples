from Ponto import Ponto

class Linha:
    def __init__(self, a: Ponto, b: Ponto):
        self.a = a
        self.b = b
        self.collide = False

    def Print(self):
        print("({ax},{ay}) -> ({bx},{by})".format(ax=self.a.x, ay=self.a.y, bx=self.b.x, by=self.b.y))