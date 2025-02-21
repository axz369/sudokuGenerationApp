from flask import Flask, render_template, request, jsonify, Response
from models.main import generate_sudoku  # models フォルダ内の main.py からインポート

app = Flask(__name__)

@app.route('/')
def home():
    # メインページを表示
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_sudoku():
    # フロントエンドから送信されたJSONデータを取得
    data = request.get_json()

    # データの検証：inputキーが含まれているかを確認
    if not data or 'input' not in data or 'board' not in data['input']:
        return jsonify({"error": "No board data received"}), 400

    # 受け取ったデータを表示
    print("Received data:")
    print(data)

    # board のデータを input キーの下から取り出す
    board = data['input']['board']
    print("Board:")
    for row in board:
        print(row)

    # generate_sudoku 関数に board を渡して結果を受け取る
    result = generate_sudoku(board)  # generate_sudoku関数に直接渡す

    print("結果を見る")
    print(result)

    # 結果がResponseオブジェクトである場合、JSONデータを取り出す
    if isinstance(result, Response):
        result = result.get_json()  # JSONデータを取り出す

    # 結果を辞書型で返す（サイズとボードを含む）
    result_data = {
        "size": len(board),  # ボードのサイズ
        "board": result  # 解決されたボード
    }

    print(type(result_data))
    # 結果をJSON形式で返す
    return jsonify(result_data)

if __name__ == '__main__':
    app.run(debug=True)
