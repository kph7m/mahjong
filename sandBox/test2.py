import random


class Tile:
    KINDS = "pinzu", "manzu", "souzu"
    LABEL = {"pinzu": "筒", "manzu": "萬", "souzu": "索"}
    NUMBERS = "一二三四五六七八九"
    WINDS = "東南西北"
    COLORS = "白發中"

    def __init__(self, kind, value, label, pic):
        self.kind = kind
        self.value = value
        self.label = label
        self.pic = pic

    def __repr__(self):
       return self.label


def mahjong_pai():
    pai = [Tile(kind, value, f"{number}{Tile.LABEL[kind]}", f"{kind}_{value}.png")
           for kind in Tile.KINDS
           for value, number in enumerate(Tile.NUMBERS, 1)]
    pai += [Tile("sufonpai", value, label, f"sufonpai_{value}.png")
            for value, label in enumerate(Tile.WINDS, 1)]
    pai += [Tile("sangenpai", value, label, f"sangenpai_{value}.png")
            for value, label in enumerate(Tile.COLORS, 1)]
    pai *= 4
    return pai


yamahai = mahjong_pai()
random.shuffle(yamahai)
print(str(yamahai))