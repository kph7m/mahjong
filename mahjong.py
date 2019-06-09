import random
import copy
import re


# 麻雀牌のクラス
class Tile:
    SUUPAI = 'pinzu', 'manzu', 'souzu'
    JIHAI = 'sufonpai', 'sangenpai'
    WINDS = '東南西北'
    COLORS = '白發中'

    def __init__(self, kind, value):
        self.kind = kind  # 麻雀牌の種類（萬子・筒子・索子・四風牌・三元牌）
        self.value = value  # 麻雀牌の値（1~9 東南西北白発中）
        self.pic = f'{kind}_{value}.png'  # 画像ファイル名

    def __repr__(self):
        return self.pic

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.pic == other.pic

    def __hash__(self):
        return hash(self.pic)

    def sort_info(self):
        if Tile.SUUPAI[0] == self.kind:
            return f'0_{self.value}'
        elif Tile.SUUPAI[1] == self.kind:
            return f'1_{self.value}'
        elif Tile.SUUPAI[2] == self.kind:
            return f'2_{self.value}'
        elif Tile.JIHAI[0] == self.kind:
            return f'3_{self.value}'
        elif Tile.JIHAI[1] == self.kind:
            return f'4_{self.value}'


# 山牌　シャッフルされた１３６個のTileオブジェクトリストを返却
def create_yamahai():
    tiles = [Tile(kind, str(value))
             for kind in Tile.SUUPAI
             for value in range(1, 1 + 9)]
    tiles += [Tile(Tile.JIHAI[0], value)
              for value, label in enumerate(Tile.WINDS, 1)]
    tiles += [Tile(Tile.JIHAI[1], value)
              for value, label in enumerate(Tile.COLORS, 1)]
    tiles *= 4

    random.shuffle(tiles)
    random.shuffle(tiles)
    random.shuffle(tiles)
    return tiles


# pic(画像ファイル名)からTileオブジェクトを作成
def tile_from_pic(pic):
    s = re.search(r'^(.+)_(.+)\.png$', pic).groups()
    return Tile(s[0], s[1])

# 通常あがり牌
class Agari:
    def __init__(self, janto, mentsu1, mentsu2, mentsu3, mentsu4):
        self.janto = janto
        self.mentsu1 = mentsu1
        self.mentsu2 = mentsu2
        self.mentsu3 = mentsu3
        self.mentsu4 = mentsu4

    def __repr__(self):
        return f'[{repr(self.janto[0])},{repr(self.janto[1])}],' \
            f'[{repr(self.mentsu1.tiles[0])},{repr(self.mentsu1.tiles[1])},{repr(self.mentsu1.tiles[2])}],' \
            f'[{repr(self.mentsu2.tiles[0])},{repr(self.mentsu2.tiles[1])},{repr(self.mentsu2.tiles[2])}],' \
            f'[{repr(self.mentsu3.tiles[0])},{repr(self.mentsu3.tiles[1])},{repr(self.mentsu3.tiles[2])}],' \
            f'[{repr(self.mentsu4.tiles[0])},{repr(self.mentsu4.tiles[1])},{repr(self.mentsu4.tiles[2])}]'


class Janto:

    def __init__(self, tiles):
        self.tiles = tiles


class Mentsu:
    KIND = 'syuntsu', 'koutsu'

    def __init__(self, kind, tiles):
        self.kind = kind
        self.tiles = tiles


class NoMentsu(Exception):
    pass


# 七対子
class Titoitsu:
    def __init__(self, l_toitsu):
        self.l_toitsu = l_toitsu

    def __repr__(self):
        return f'[{repr(self.l_toitsu[0])},{repr(self.l_toitsu[0])}],' \
            f'[{repr(self.l_toitsu[1])},{repr(self.l_toitsu[1])}],' \
            f'[{repr(self.l_toitsu[2])},{repr(self.l_toitsu[2])}],' \
            f'[{repr(self.l_toitsu[3])},{repr(self.l_toitsu[3])}],' \
            f'[{repr(self.l_toitsu[4])},{repr(self.l_toitsu[4])}],' \
            f'[{repr(self.l_toitsu[5])},{repr(self.l_toitsu[5])}],' \
            f'[{repr(self.l_toitsu[6])},{repr(self.l_toitsu[6])}]'


# 国士無双
class Kokushimusou:
    def __init__(self, l_tile):
        self.l_tile = l_tile

    def __repr__(self):
        return f'{self.l_tile}'


# あがり判定
def judge(tehai):
    agari_hai = []

    # 雀頭の種類
    l_janto = sorted([x for x in set(tehai) if tehai.count(x) >= 2], key=lambda hai: f'{hai.kind}{hai.value}')
    if len(l_janto) == 0:
        return agari_hai

    # 国士無双
    if check_kokushimusou(tehai, l_janto):
        return Kokushimusou(tehai)

        # 七対子
    if len(l_janto) == 7:
        agari_hai.append(Titoitsu(l_janto))

    # 通常役
    for janto in l_janto:
        mentsu_kouho = copy.deepcopy(tehai)
        mentsu_kouho.remove(janto)
        mentsu_kouho.remove(janto)

        mentsu_kouho.sort(key=lambda hai: f'{hai.kind}{hai.value}')

        # 刻子の種類
        l_koutsu = sorted([x for x in set(mentsu_kouho) if mentsu_kouho.count(x) >= 3],
                          key=lambda hai: f'{hai.kind}{hai.value}')

        # 刻子が０個のパターン
        agari_hai.extend(agari_koutsu0(mentsu_kouho, janto))

        # 刻子が１個のパターン
        agari_hai.extend(agari_koutsu1(mentsu_kouho, janto, l_koutsu))

        # 刻子が２個のパターン
        agari_hai.extend(agari_koutsu2(mentsu_kouho, janto, l_koutsu))

        # 刻子が３個のパターン
        agari_hai.extend(agari_koutsu3(mentsu_kouho, janto, l_koutsu))

        # 刻子が４個のパターン
        agari_hai.extend(agari_koutsu4(janto, l_koutsu))

    return len(agari_hai) > 0


# 刻子が０個のあがりパターン
def agari_koutsu0(mentsu_kouho, janto):
    try:
        hanteiyou = copy.deepcopy(mentsu_kouho)

        first = find_one_syuntu(hanteiyou)
        hanteiyou.remove(first.tiles[0])
        hanteiyou.remove(first.tiles[1])
        hanteiyou.remove(first.tiles[2])

        second = find_one_syuntu(hanteiyou)
        hanteiyou.remove(second.tiles[0])
        hanteiyou.remove(second.tiles[1])
        hanteiyou.remove(second.tiles[2])

        third = find_one_syuntu(hanteiyou)
        hanteiyou.remove(third.tiles[0])
        hanteiyou.remove(third.tiles[1])
        hanteiyou.remove(third.tiles[2])

        fourth = find_one_syuntu(hanteiyou)

        return [Agari([janto for x in range(2)], first, second, third, fourth)]

    except NoMentsu:
        return []


# 刻子が１個のあがりパターン
def agari_koutsu1(mentsu_kouho, janto, l_koutsu):
    if len(l_koutsu) < 1:
        return []

    result = []
    for koutsu in l_koutsu:
        try:
            hanteiyou = copy.deepcopy(mentsu_kouho)

            first = Mentsu(Mentsu.KIND[1], [koutsu for x in range(3)])
            hanteiyou.remove(first.tiles[0])
            hanteiyou.remove(first.tiles[1])
            hanteiyou.remove(first.tiles[2])

            second = find_one_syuntu(hanteiyou)
            hanteiyou.remove(second.tiles[0])
            hanteiyou.remove(second.tiles[1])
            hanteiyou.remove(second.tiles[2])

            third = find_one_syuntu(hanteiyou)
            hanteiyou.remove(third.tiles[0])
            hanteiyou.remove(third.tiles[1])
            hanteiyou.remove(third.tiles[2])

            fourth = find_one_syuntu(hanteiyou)

            result.append(Agari([janto for x in range(2)], first, second, third, fourth))

        except NoMentsu:
            continue

    return result


# 刻子が２個のあがりパターン
def agari_koutsu2(mentsu_kouho, janto, l_koutsu):
    if len(l_koutsu) < 2:
        return []

    result = []
    for i in range(len(l_koutsu) - 1):
        for j in range(i + 1, len(l_koutsu)):
            try:
                hanteiyou = copy.deepcopy(mentsu_kouho)

                first = Mentsu(Mentsu.KIND[1], [l_koutsu[i] for x in range(3)])
                hanteiyou.remove(first.tiles[0])
                hanteiyou.remove(first.tiles[1])
                hanteiyou.remove(first.tiles[2])

                second = Mentsu(Mentsu.KIND[1], [l_koutsu[j] for x in range(3)])
                hanteiyou.remove(second.tiles[0])
                hanteiyou.remove(second.tiles[1])
                hanteiyou.remove(second.tiles[2])

                third = find_one_syuntu(hanteiyou)
                hanteiyou.remove(third.tiles[0])
                hanteiyou.remove(third.tiles[1])
                hanteiyou.remove(third.tiles[2])

                fourth = find_one_syuntu(hanteiyou)

                result.append(Agari([janto for x in range(2)], first, second, third, fourth))

            except NoMentsu:
                continue

    return result


# 刻子が３個のあがりパターン
def agari_koutsu3(mentsu_kouho, janto, l_koutsu):
    if len(l_koutsu) != 3:
        return []

    try:
        hanteiyou = copy.deepcopy(mentsu_kouho)

        first = Mentsu(Mentsu.KIND[1], [l_koutsu[0] for x in range(3)])
        hanteiyou.remove(first.tiles[0])
        hanteiyou.remove(first.tiles[1])
        hanteiyou.remove(first.tiles[2])

        second = Mentsu(Mentsu.KIND[1], [l_koutsu[1] for x in range(3)])
        hanteiyou.remove(second.tiles[0])
        hanteiyou.remove(second.tiles[1])
        hanteiyou.remove(second.tiles[2])

        third = Mentsu(Mentsu.KIND[1], [l_koutsu[2] for x in range(3)])
        hanteiyou.remove(third.tiles[0])
        hanteiyou.remove(third.tiles[1])
        hanteiyou.remove(third.tiles[2])

        fourth = find_one_syuntu(hanteiyou)

        return [Agari([janto for x in range(2)], first, second, third, fourth)]

    except NoMentsu:
        return []


# 刻子が４個のあがりパターン
def agari_koutsu4(janto, l_koutsu):
    if len(l_koutsu) != 4:
        return []

    return [Agari([janto for x in range(2)], Mentsu(Mentsu.KIND[1], [l_koutsu[0] for x in range(3)]),
                  Mentsu(Mentsu.KIND[1], [l_koutsu[1] for x in range(3)]),
                  Mentsu(Mentsu.KIND[1], [l_koutsu[2] for x in range(3)]),
                  Mentsu(Mentsu.KIND[1], [l_koutsu[3] for x in range(3)]))]


# 国士無双のチェック（前提として雀頭があること）
def check_kokushimusou(tehai, l_koutsu):
    if len(l_koutsu) != 1:
        return []

    if Tile(Tile.SUUPAI[0], '1') in tehai \
            and Tile(Tile.SUUPAI[0], '9') in tehai \
            and Tile(Tile.SUUPAI[1], '1') in tehai \
            and Tile(Tile.SUUPAI[1], '9') in tehai \
            and Tile(Tile.SUUPAI[2], '1') in tehai \
            and Tile(Tile.SUUPAI[2], '9') in tehai \
            and Tile(Tile.JIHAI[0], Tile.WINDS[0]) in tehai \
            and Tile(Tile.JIHAI[0], Tile.WINDS[1]) in tehai \
            and Tile(Tile.JIHAI[0], Tile.WINDS[2]) in tehai \
            and Tile(Tile.JIHAI[0], Tile.WINDS[3]) in tehai \
            and Tile(Tile.JIHAI[1], Tile.COLORS[0]) in tehai \
            and Tile(Tile.JIHAI[1], Tile.COLORS[1]) in tehai \
            and Tile(Tile.JIHAI[1], Tile.COLORS[2]) in tehai:
        return True


# 順子をひとつ見つける
def find_one_syuntu(hanteiyou):
    hanteiyou.sort(key=lambda hai: f'{hai.kind}{hai.value}')
    for hanteiyou_one_tile in hanteiyou:
        syuntsu_kouho = create_syuntsu(hanteiyou_one_tile)
        if syuntsu_kouho is None:
            continue
        if syuntsu_kouho[1] in hanteiyou and syuntsu_kouho[2] in hanteiyou:
            return Mentsu(Mentsu.KIND[0], syuntsu_kouho)
    raise NoMentsu()


# 自身を一番最初とした順子を返却
def create_syuntsu(tile):
    if tile.kind in Tile.SUUPAI and int(tile.value) <= 7:
        return [Tile(tile.kind, str(value))
                for value in range(int(tile.value), int(tile.value) + 3)]


def test():
    l_haipai = []
    for pattern in ['23333444556688', '22333456667788', '22344445556677', '11123334445577',
                    '22223333444556', '11222345556677', '22333344555667', '11333445566678',
                    '11122223334455', '22555566677788', '23333444555566', '22566667778899',
                    '22444567778899', '22444455666778', '12222333445599', '22223344455688',
                    '11123334445555', '33344555566678', '44455667778999', '11112233344566',
                    '11444556667778', '11225566778899', '44445555666778', '12222333445588',
                    '22234555667777', '33345666778888', '11122334445666', '22223334445588',
                    '33345666777788', '11122334445677', '22233345556677', '11223344667799',
                    '11123444555566', '44455567778899', '33444455666778', '22234445556666',
                    '11222334455567', '44456667778888', '11123344455688', '11222334445556',
                    '11444566777889', '11123334445588', '11333344555667', '22234555666677',
                    '11122333444566', '44566667778899', '55666677788899', '33334455566799',
                    '11555667778889', '11333455566677', '22223344455699', '33344445556677',
                    '33555566777889', '22233445556799', '11122333444588', '11122223344456',
                    '22223334445599', '34444555666677', '44445566677899', '55556666777889',
                    '22444556677789', '11122333444599', '11112223334499', '11334455667799',
                    '33345566677899', '11123344455666', '33334445556699', '33444566777889',
                    '11122233444556', '11666677788899', '33344555666788', '22233334445556',
                    '11123334445566', '11566667778899', '11224466778899', '11224455667799',
                    '22444556667778', '12222333444455', '22234445556677', '33444455566677',
                    '22333344455566', '11123334445599', '33444556677789', '11122333444577',
                    '11112223334466', '11122223334445', '22234455566667', '22223334445577',
                    '11223355668899', '11444455666778', '11123444556688', '44555667778889',
                    '11122334445699', '11333456667788', '11112223334488', '55566667778889',
                    '11233334445566', '11334455668899', '33345556667799', '22233344555667',
                    '34444555667799', '11223344557799', '11224455667788', '22333445556667',
                    '22234445556688', '22234444555667', '11224455668899', '22234555667799',
                    '11112233344599', '33344445556667', '44445566677888', '11112223334477',
                    '55556677788999', '11112233344588', '11112222333445', '22234455566799',
                    '11123444556699', '33555667778889', '22333445566678', '33566667778899',
                    '12222333445577', '22444566777889', '22233444455567', '44455666677789',
                    '22555677788899', '44455556677789', '44555566777889', '22233445556788',
                    '11224455778899', '44455566777889', '33444567778899', '11444566677788',
                    '44456667778899', '22335566778899', '33334444555667', '11223344668899',
                    '22234455566777', '44456777888899', '33344556667899', '44455556667778',
                    '11223344557788', '33666677788899', '11112233344555', '55567778889999',
                    '11444455566677', '11455556667788', '33345556667788', '33344456667788',
                    '22233444555699', '44555566677788', '11222233444556', '11122333344456',
                    '11344445556677', '11222344555667', '44445556667799', '33555677788899',
                    '22233444555677', '11123344455699', '11333445556667', '44456677788889',
                    '22333455666778', '33455556667788', '11123344455556', '11334466778899',
                    '33555566677788', '11444556677789', '44456677788999', '11122234445566',
                    '22555667778889', '22455556667788', '33444556667778', '22233445556777',
                    '33344445566678', '11555566677788', '33344555666799', '22555566777889',
                    '33345566677778', '33345556667777', '33334455566788', '22233334455567',
                    '22234445556699', '33334445556688', '11333344455566', '44455556667788',
                    '33345566677888', '11123333444556', '33344556667888', '11222344455566',
                    '33345555666778', '22234455566788', '22333455566677', '44455666777899',
                    '23333444556699', '11333455666778', '11223344558899', '11444567778899',
                    '11335566778899', '33334455566777', '45555666777788', '44456666777889',
                    '11123344455677', '33444566677788', '11123444556666', '22444455566677',
                    '22223344455666', '22233444555688', '11222233344455', '44456777889999',
                    '44555677788899', '22444566677788', '22666677788899', '22233334445566',
                    '44666677788899', '11122334445688', '22334455668899', '33344455666778',
                    '56666777888899', '11555566777889', '55566667778899', '11112233344577',
                    '22223344455677', '11555677788899']:
        l_haipai.append([Tile('manzu', value)
                         for value in list(pattern)])
    l_haipai.append(
        [Tile(Tile.SUUPAI[0], '1'), Tile(Tile.SUUPAI[0], '9'), Tile(Tile.SUUPAI[1], '1'), Tile(Tile.SUUPAI[1], '9'),
         Tile(Tile.SUUPAI[2], '1'), Tile(Tile.SUUPAI[2], '9'), Tile(Tile.JIHAI[0], Tile.WINDS[0]),
         Tile(Tile.JIHAI[0], Tile.WINDS[1]), Tile(Tile.JIHAI[0], Tile.WINDS[2]), Tile(Tile.JIHAI[0], Tile.WINDS[3]),
         Tile(Tile.JIHAI[1], Tile.COLORS[0]), Tile(Tile.JIHAI[1], Tile.COLORS[1]),
         Tile(Tile.JIHAI[1], Tile.COLORS[2]), Tile(Tile.SUUPAI[0], '1')])
    for haipai in l_haipai:
        print(f'配牌:{haipai}')
        print(f'上り:{judge(haipai)}')


if __name__ == '__main__':
    test()
