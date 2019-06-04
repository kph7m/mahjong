from flask import Flask
import mahjong

app = Flask(__name__)

yamahai = []
haipai = []

# 配牌
@app.route('/')
def main():
    global haipai
    global yamahai
    yamahai = mahjong.create_yamahai()
    haipai = [yamahai.pop(0) for i in range(14)]  # 配牌
    haipai.sort(key=lambda hai: hai.sort_info())  # 理牌

    # 画像表示
    return ''.join(map(lambda i: f'<a href="/change/{i}"><img src=/static/pic/{haipai[i].pic}></a>',
                       range(len(haipai))))


# 自摸
@app.route('/change/<int:position>')
def change(position):
    haipai.pop(position)  # 打牌
    haipai.sort(key=lambda hai: hai.sort_info())  # 理牌

    haipai.append(yamahai.pop(0))  # 自摸

    if mahjong.judge(haipai):  # あがり判定
        return ''.join(map(lambda i: f'<img src=/static/pic/{haipai[i].pic}>', range(len(haipai)-1))) \
               + f'&nbsp;<img src=/static/pic/{haipai[len(haipai) - 1].pic}>' \
               + f'<br><a href="/"><img src=/static/pic/win.png></a>'
    else:
        return ''.join(map(lambda i: f'<a href="/change/{i}"><img src=/static/pic/{haipai[i].pic}></a>',
                           range(len(haipai)-1)))\
               + f'&nbsp;<a href="/change/{len(haipai)-1}"><img src=/static/pic/{haipai[len(haipai)-1].pic}></a>'

if __name__ == '__main__':
    app.run(port=8080)
