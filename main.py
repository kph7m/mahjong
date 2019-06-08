from flask import Flask, render_template
import mahjong

app = Flask(__name__)

yamahai = []
tehai = []
sutehai = []

# 配牌
@app.route('/')
def main():
    global tehai
    global yamahai
    yamahai = mahjong.create_yamahai()
    tehai = [yamahai.pop(0) for i in range(13)]  # 配牌

    tehai.sort(key=lambda hai: hai.sort_info())  # 理牌
    tehai.append(yamahai.pop(0))  # 自摸

    # 画像表示
    # return ''.join(map(lambda i: f'<a href="/change/{i}"><img src=/static/pic/{tehai[i].pic}></a>',
    #                    range(len(tehai))))

    return render_template('main.html', tehai=tehai, win=mahjong.judge(tehai))


# 自摸
@app.route('/change/<int:position>')
def change(position):
    sutehai.append(tehai.pop(position))  # 打牌
    tehai.sort(key=lambda hai: hai.sort_info())  # 理牌

    tehai.append(yamahai.pop(0))  # 自摸

    return render_template('main.html', tehai=tehai, sutehai=sutehai, win=mahjong.judge(tehai))
    # if mahjong.judge(tehai):  # あがり判定
    #     return ''.join(map(lambda i: f'<img src=/static/pic/{tehai[i].pic}>', range(len(tehai) - 1))) \
    #            + f'&nbsp;<img src=/static/pic/{tehai[len(tehai) - 1].pic}>' \
    #            + f'<br><a href="/"><img src=/static/pic/win.png></a>'
    # else:
    #     return ''.join(map(lambda i: f'<a href="/change/{i}"><img src=/static/pic/{tehai[i].pic}></a>',
    #                        range(len(tehai) - 1)))\
    #            + f'&nbsp;<a href="/change/{len(tehai) - 1}"><img src=/static/pic/{tehai[len(tehai) - 1].pic}></a>'


if __name__ == '__main__':
    app.run(port=8080)
