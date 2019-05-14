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
        self.pic = pic  #画像ファイル名

    def __repr__(self):
        return repr((self.kind, self.value, self.pic))

    def create_img_tag(self):
        return f'<img src=/static/pic/{self.pic}>'

#山牌
def mahjong_pai():
    pai = [Tile(kind, value, f"{kind}_{value}.png")
           for kind in Tile.NUMBERS
           for value in range(1, 9+1)]
    pai += [Tile("sufonpai", value, f"sufonpai_{value}.png")
            for value, label in enumerate(Tile.WINDS, 1)]
    pai += [Tile("sangenpai", value, f"sangenpai_{value}.png")
            for value, label in enumerate(Tile.COLORS, 1)]
    pai *= 4

    random.shuffle(pai)
    return pai


yamahai = mahjong_pai()

@app.route('/')
def main():

    img_tags = ''
    for i in range(14):
        tile = yamahai.pop(0)  #山牌から一つ取り出す
        img_tags = img_tags + tile.create_img_tag()#画像出力用のHTMLタグ作成

    return img_tags


if __name__ == '__main__':
    app.run(port=8080)
