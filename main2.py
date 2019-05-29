from flask import Flask
import random
import copy
from functools import reduce

app = Flask(__name__)


# 麻雀牌のクラス
class Tile:
    NUMBERS = "pinzu", "manzu", "souzu"
    WINDS = "東南西北"
    COLORS = "白發中"

    def __init__(self, kind, value):
        self.kind = kind  # 麻雀牌の種類（萬子・筒子・索子・四風牌・三元牌）
        self.value = value  # 麻雀牌の値（1~9 東南西北白発中）
        self.pic = f"{kind}_{value}.png"  # 画像ファイル名

    def __repr__(self):
        return self.pic

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.pic == other.pic

    def __hash__(self):
        return hash(self.pic)

    # 自身を一番最初とした順子を返却
    def create_syuntu(self):
        if Tile.NUMBERS.contains(self.kind) and int(self.value) <= 7:
            return [Tile(self.kind, str(value))
                    for value in range(self.value, self.value + 3)]

class Agari:
    def __init__(self, janto, mentsu1, mentsu2, mentsu3, mentsu4):
        self.janto = janto
        self.mentsu1 = mentsu1
        self.mentsu2 = mentsu2
        self.mentsu3 = mentsu3
        self.mentsu4 = mentsu4

    def __repr__(self):
        return f"[{repr(self.janto[0])},{repr(self.janto[1])}] \
                ,[{repr(self.mentsu1[0])},{repr(self.mentsu1[1])},{repr(self.mentsu1[1])}] \
                ,[{repr(self.mentsu2[0])},{repr(self.mentsu2[1])},{repr(self.mentsu2[1])}] \
                ,[{repr(self.mentsu3[0])},{repr(self.mentsu3[1])},{repr(self.mentsu3[1])}] \
                ,[{repr(self.mentsu4[0])},{repr(self.mentsu4[1])},{repr(self.mentsu4[1])}]"




class Janto:

    def __init__(self, tiles):
        self.tiles = tiles

class Mentsu:
    KIND = "syuntu", "koutsu"

    def __init__(self, kind, tiles):
        self.kind = kind
        self.tiles = tiles


class NoMentsu(Exception):
    pass


# 山牌　シャッフルされた１３６個のTileオブジェクトリストを返却
def create_yamahai():
    tiles = [Tile(kind, str(value))
             for kind in Tile.NUMBERS
             for value in range(1, 1 + 9)]
    tiles += [Tile("sufonpai", value)
              for value, label in enumerate(Tile.WINDS, 1)]
    tiles += [Tile("sangenpai", value)
              for value, label in enumerate(Tile.COLORS, 1)]
    tiles *= 4

    random.shuffle(tiles)
    return tiles


yamahai = create_yamahai()  # 山牌作成

haipai = [
    Tile('manzu', '2'),
    Tile('manzu', '3'),
    Tile('manzu', '3'),
    Tile('manzu', '3'),
    Tile('manzu', '3'),
    Tile('manzu', '4'),
    Tile('manzu', '4'),
    Tile('manzu', '5'),
    Tile('manzu', '5'),
    Tile('manzu', '5'),
    Tile('manzu', '6'),
    Tile('manzu', '6'),
    Tile('manzu', '8'),
    Tile('manzu', '8')
]


@app.route('/')
def main():
    #    test.sort(key=lambda hai: f'{hai.kind}{hai.value}')  # 理牌

    agari_hai = []
    # 牌の種類だけ抜き出し
    l_unique = sorted(list(set(haipai)), key=lambda hai: f'{hai.kind}{hai.value}')
    print(l_unique)

    # 雀頭の種類
    l_janto = sorted([x for x in set(haipai) if haipai.count(x) >= 2])
    #    l_duplicate.sort(key=lambda hai: f'{hai.kind}{hai.value}')
    print(l_janto)
    for janto in l_janto:
        print(f'雀頭:{janto}')

        # 刻子の種類
        l_koutsu = [x for x in set(haipai) if haipai.count(x) >= 3]
        print(f'刻子:{l_koutsu}')

        # 刻子が０個のパターン
        agari_hai.append(agari_koutsu0(haipai, janto))

        # 刻子が１個のパターン
        agari_hai.append(agari_koutsu1(haipai, janto, l_koutsu))

        # 刻子が２個のパターン(刻子を3つ取得可能な場合にそこから２つ取得する場合を含む)
        agari_hai.append(agari_koutsu2(l_koutsu, janto, l_koutsu))

        # 刻子が３個のパターン
        agari_hai.append(agari_koutsu3(l_koutsu, janto, l_koutsu))

        # 刻子が４個のパターン
        agari_hai.append(agari_koutsu4(l_koutsu, janto))


def agari_koutsu0(haipai, janto):
    hannteiyou = copy.deepcopy(haipai)

    hannteiyou.remove(janto)
    hannteiyou.remove(janto)

    try:
        one = find_one_syuntu(hannteiyou)
        hannteiyou.remone(one.tiles[0])
        hannteiyou.remone(one.tiles[1])
        hannteiyou.remone(one.tiles[2])

        two = find_one_syuntu(hannteiyou)
        hannteiyou.remone(two.tiles[0])
        hannteiyou.remone(two.tiles[1])
        hannteiyou.remone(two.tiles[2])

        three = find_one_syuntu(hannteiyou)
        hannteiyou.remone(three.tiles[0])
        hannteiyou.remone(three.tiles[1])
        hannteiyou.remone(three.tiles[2])

        four = find_one_syuntu(hannteiyou)
        hannteiyou.remone(four.tiles[0])
        hannteiyou.remone(four.tiles[1])
        hannteiyou.remone(four.tiles[2])

        return Agari([janto * 2], one, two, three, four)
    except NoMentsu:
        return []

def agari_koutsu1(haipai, l_koutsu, janto):
    if len(l_koutsu) < 1:
        return []

    hannteiyou = copy.deepcopy(haipai)

    hannteiyou.remove(janto)
    hannteiyou.remove(janto)

    result=[]
    for koutsu in l_koutsu:
        try:
            one = Mentsu([koutsu * 3], Mentsu.KIND[1])
            hannteiyou.remone(one[0])
            hannteiyou.remone(one[1])
            hannteiyou.remone(one[2])

            two = find_one_syuntu(hannteiyou)
            hannteiyou.remone(two[0])
            hannteiyou.remone(two[1])
            hannteiyou.remone(two[2])

            three = find_one_syuntu(hannteiyou)
            hannteiyou.remone(three[0])
            hannteiyou.remone(three[1])
            hannteiyou.remone(three[2])

            four = find_one_syuntu(hannteiyou)
            hannteiyou.remone(four[0])
            hannteiyou.remone(four[1])
            hannteiyou.remone(four[2])

            result.append(Agari([janto*2],one,two,three,four))

        except NoMentsu:
            pass

    return result



def agari_koutsu2(haipai, l_koutsu, janto):
    if len(l_koutsu) < 2:
        return []

    hannteiyou = copy.deepcopy(haipai)

    hannteiyou.remove(janto)
    hannteiyou.remove(janto)

    result = []
    for i in range(len(l_koutsu)):
        for j in range(i + 1, len(l_koutsu)):
            try:
                one = Mentsu([l_koutsu[i] * 3], Mentsu.KIND[1])
                hannteiyou.remone(one[0])
                hannteiyou.remone(one[1])
                hannteiyou.remone(one[2])

                two = Mentsu([l_koutsu[j] * 3], Mentsu.KIND[1])
                hannteiyou.remone(two[0])
                hannteiyou.remone(two[1])
                hannteiyou.remone(two[2])

                three = find_one_syuntu(hannteiyou)
                hannteiyou.remone(three[0])
                hannteiyou.remone(three[1])
                hannteiyou.remone(three[2])

                four = find_one_syuntu(hannteiyou)
                hannteiyou.remone(four[0])
                hannteiyou.remone(four[1])
                hannteiyou.remone(four[2])
                result.append(Agari([janto * 2], one, two, three, four))

            except NoMentsu:
                pass

    return result


def agari_koutsu3(haipai, l_koutsu, janto):
    if len(l_koutsu) != 3:
        return []

    hannteiyou = copy.deepcopy(haipai)

    hannteiyou.remove(janto)
    hannteiyou.remove(janto)

    try:
        one = Mentsu([l_koutsu[0] * 3], Mentsu.KIND[1])
        hannteiyou.remone(one[0])
        hannteiyou.remone(one[1])
        hannteiyou.remone(one[2])

        two = [l_koutsu[1] * 3]
        hannteiyou.remone(two[0])
        hannteiyou.remone(two[1])
        hannteiyou.remone(two[2])

        three = [l_koutsu[2] * 3]
        hannteiyou.remone(three[0])
        hannteiyou.remone(three[1])
        hannteiyou.remone(three[2])

        four = find_one_syuntu(hannteiyou)
        hannteiyou.remone(four[0])
        hannteiyou.remone(four[1])
        hannteiyou.remone(four[2])

        return Agari([janto * 2], one, two, three, four)

    except NoMentsu:
        pass

def agari_koutsu4(l_koutsu, janto):
    if len(l_koutsu) != 4:
        return []

    return Agari([janto * 2], [l_koutsu[0] * 3], [l_koutsu[1] * 3], [l_koutsu[2] * 3], [l_koutsu[3] * 3])


# 順子をひとつ見つける
def find_one_syuntu(hannteiyou):
    hannteiyou.sort(key=lambda hai: f'{hai.kind}{hai.value}')
    for haipai_one_tile in hannteiyou:
        syuntu = haipai_one_tile.create_syuntu()
        for syuntu_one_tile in syuntu:
            if syuntu_one_tile not in hannteiyou:
                syuntu = None
                break
        if syuntu :
            return Mentsu(syuntu, Mentsu.KIND[0])
    raise NoMentsu()

# def find_koutsu(hannteiyou):
#     for i in range(len(hannteiyou) - 2):
#         if Tile.NUMBERS.contains(hannteiyou[i].kind) \
#                 and hannteiyou.contains(Tile(hannteiyou[i].kind, str(int(hannteiyou[i].value) + 1))) \
#                 and hannteiyou.contains(Tile(hannteiyou[i].kind, str(int(hannteiyou[i].value) + 2))):
#             return Tile(hannteiyou[i])


if __name__ == '__main__':
    main()
