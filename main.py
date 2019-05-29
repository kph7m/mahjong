from flask import Flask
import random

app = Flask(__name__)


# 麻雀牌のクラス
class Tile:
    NUMBERS = "pinzu", "manzu", "souzu"
    WINDS = "東南西北"
    COLORS = "白發中"

    def __init__(self, kind, value, pic):
        self.kind = kind  # 麻雀牌の種類（萬子・筒子・索子・四風牌・三元牌）
        self.value = value  # 麻雀牌の値（1~9 東南西北白発中）
        self.pic = pic  # 画像ファイル名

    def __repr__(self):
        return f'({self.kind}, {self.value}, {self.pic})\n'


# 山牌　シャッフルされた１３６個のTileオブジェクトリストを返却
def create_yamahai():
    tiles = [Tile(kind, value, f"{kind}_{value}.png")
             for kind in Tile.NUMBERS
             for value in range(1, 9 + 1)]
    tiles += [Tile("x_sufonpai", value, f"sufonpai_{value}.png")
              for value, label in enumerate(Tile.WINDS, 1)]
    tiles += [Tile("y_sangenpai", value, f"sangenpai_{value}.png")
              for value, label in enumerate(Tile.COLORS, 1)]
    tiles *= 4

    random.shuffle(tiles)
    return tiles


yamahai = create_yamahai() #山牌作成

test = [
          Tile('manzu', '2', 'manzu_2.png')
        , Tile('manzu', '3', 'manzu_3.png')
        , Tile('manzu', '3', 'manzu_3.png')
        , Tile('manzu', '3', 'manzu_3.png')
        , Tile('manzu', '3', 'manzu_3.png')
        , Tile('manzu', '4', 'manzu_4.png')
        , Tile('manzu', '4', 'manzu_4.png')
        , Tile('manzu', '5', 'manzu_5.png')
        , Tile('manzu', '5', 'manzu_5.png')
        , Tile('manzu', '5', 'manzu_5.png')
        , Tile('manzu', '6', 'manzu_6.png')
        , Tile('manzu', '6', 'manzu_6.png')
        , Tile('manzu', '6', 'manzu_6.png')
        , Tile('manzu', '6', 'manzu_6.png')
        , Tile('manzu', '8', 'manzu_8.png')
        , Tile('manzu', '8', 'manzu_8.png')
    ]
@app.route('/')
def main():
    haipai = [yamahai.pop(0) for i in range(14)]  # 配牌

    haipai.sort(key=lambda hai: f'{hai.kind}{hai.value}')  # 理牌

    test.sort(key=lambda hai: f'{hai.kind}{hai.value}')  # 理牌


    return ''.join(map(lambda tile: f'<img src=/static/pic/{tile.pic}>', haipai))  # 画像表示


if __name__ == '__main__':
    app.run(port=8080)
