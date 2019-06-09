from flask import Flask, render_template, request
import mahjong
import os

app = Flask(__name__)

# 配牌
@app.route('/')
def main():
    yamahai = mahjong.create_yamahai()  # 山牌
    tehai = [yamahai.pop(0) for i in range(13)]  # 配牌

    tehai.sort(key=lambda hai: hai.sort_info())  # 理牌
    tehai.append(yamahai.pop(0))  # 自摸

    return render_template('main.html', tehai=tehai, win=mahjong.judge(tehai))


# 自摸
@app.route('/change', methods=['POST'])
def change():
    dahai = mahjong.tile_from_pic(request.form['dahai']) # 打牌
    sutehai = [mahjong.tile_from_pic(pic) for pic in request.form.getlist('sutehai')] # 捨て牌
    tehai = [mahjong.tile_from_pic(pic) for pic in request.form.getlist('tehai')] # 手牌

    tehai.remove(dahai)# 手牌から打牌を削除
    sutehai.append(dahai)# 捨て牌に打牌を追加

    yamahai = mahjong.create_yamahai()  # 山牌再作成
    for tile in sutehai + tehai:  # 山牌から捨て牌と手牌を削除
        yamahai.remove(tile)

    tehai.sort(key=lambda hai: hai.sort_info())  # 理牌
    tehai.append(yamahai.pop(0))  # 自摸

    return render_template('main.html', tehai=tehai, sutehai=sutehai, win=mahjong.judge(tehai))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
