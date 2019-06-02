from flask import Flask
import mahjong

app = Flask(__name__)

yamahai = mahjong.create_yamahai()

@app.route('/')
def main():
    haipai = [yamahai.pop(0) for i in range(14)]  # 配牌
    haipai.sort(key=lambda hai: f'{hai.kind}{hai.value}')  # 理牌

    return ''.join(map(lambda tile: f'<img src=/static/pic/{tile.pic}>', haipai))  # 画像表示


if __name__ == '__main__':
    app.run(port=8080)
