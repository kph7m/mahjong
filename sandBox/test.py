import random


class Tile:
    NUMBERS = "pinzu", "manzu", "souzu"
    WINDS = "東南西北"
    COLORS = "白發中"

    def __init__(self, kind, value, pic):
        self.kind = kind
        self.value = value
        self.pic = pic

    def __repr__(self):
        return f"Tile({repr(self.kind)}, {repr(self.value)}, {repr(self.pic)})"

    def create_img_tag(self):
        return f'<img src=/static/pic/{self.pic}>'


def mahjong_pai():
    pai = [Tile(kind, value, f"{kind}_{value}.png")
           for kind in Tile.NUMBERS
           for value in range(1, 9+1)]
    pai += [Tile("sufonpai", value, f"sufonpai_{value}.png")
            for value, label in enumerate(Tile.WINDS, 1)]
    pai += [Tile("sangenpai", value, f"sangenpai_{value}.png")
            for value, label in enumerate(Tile.COLORS, 1)]
    pai *= 4

    return pai




yamahai = mahjong_pai()
random.shuffle(yamahai)


img_tags = [yamahai.pop(0).create_img_tag() for i in range(14)]

''.join(img_tags)
print(''.join(img_tags))
print(yamahai)
yamahai.sort(key=lambda hai: f'{hai.kind}{hai.value}')
print(yamahai)