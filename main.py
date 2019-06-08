from flask import Flask, render_template, request
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
@app.route('/change', methods=['POST'])
def change():
    dahai = request.form['dahai']
    v_sutehai = request.form.getlist('sutehai')
    v_tehai = request.form.getlist('tehai')



    # sutehai.append(tehai.pop(position))  # 打牌
    # tehai.sort(key=lambda hai: hai.sort_info())  # 理牌
    #
    # tehai.append(yamahai.pop(0))  # 自摸

    return render_template('main.html', tehai=tehai, sutehai=sutehai, win=mahjong.judge(tehai))



if __name__ == '__main__':
    app.run(port=8080)
