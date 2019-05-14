from pathlib import Path
import os
import re


p = Path("/Users/itoutoshiya/PycharmProjects/mahjong/static/pic")
files = sorted(p.glob("*"))         #ファイルの一覧をソートして取得

for file_ in files:
    name = file_.name
#    Tile('manzu', '1', 'manzu_1.png')
    match_kind = re.search(r"^(.*?)_", name)
    match_val = re.search(r"_(.*?)\.", name)

    for i in range(4):
        print(f", Tile('{match_kind.group(1)}', '{match_val.group(1)}', '{name}')")
