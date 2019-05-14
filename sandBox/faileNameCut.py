# from pathlib import Path
# import os
# import re
#
# p = Path("/Users/Shared/Work/Ok")  #画像のあるディレクトリを取得
# files = sorted(p.glob("*"))        #ファイルの一覧をソートして取得
#
# syurui = ''                        #種類取得用一時変数
# i = 0                              #種類ごとの連番
# for file in files:                 #1ファイルづつループ
#     if file.name.startswith("."):  #隠しファイルに対しては処理を行わない
#         continue
#
#     oldFilePath = file.__str__()   #現在のファイルフルパス取得
#     print(oldFilePath)
#
#     parentDir = file.parent.__str__()#親ディレクトリ名取得
#     anchor = file.anchor             #ファイルパスの区切り文字取得
#     fileName = file.name             #ファイル名称取得
#     suffix = file.suffix             #ファイルの拡張子取得
#
#     match = re.search(r'_(.*?)-', fileName) #正規表現
#     if syurui != match.group(1):     #種類ごとに連番iをカウント
#         syurui = match.group(1)
#         i = 0
#     i = i+1
#
#     newFileName = syurui+'_' + i.__str__() + suffix #変更後のファイル名
#     newFilePath = parentDir+anchor + newFileName    #変更後のファイルフルパス
#     print(newFilePath)
#
#     os.rename(oldFilePath,newFilePath)              #ファイル名の変更

#リファクタリング後
from pathlib import Path
import os
import re

p = Path("/Users/Shared/Work/Ok")   #画像のあるディレクトリを取得
files = sorted(p.glob("*"))         #ファイルの一覧をソートして取得

kind = ""                           #種類
count = 0                           #種類ごとの連番
for file_ in files:
    name = file_.name
    old_path = str(file_.parent)            #現在のファイルフルパス取得
    hash(file_)
    print(old_path)

    parent = str(file_.parent)       # 親ディレクトリ名取得
    anchor = file_.anchor            # ファイルパスの区切り文字取得
    suffix = file_.suffix            # ファイルの拡張子取得

    match = re.search(r"_(.*?)-", name)  # 正規表現　_から-の間が牌の種類名
    if kind != match.group(1):
        kind = match.group(1)
        count = 0
    count += 1

    new_name = f"{kind}_{count}{suffix}"      # 変更後のファイル名
    new_path = f"{parent}{anchor}{new_name}"  # 変更後のファイルフルパス
    print(new_path)

    os.rename(old_path, new_path)  # ファイル名の変更
