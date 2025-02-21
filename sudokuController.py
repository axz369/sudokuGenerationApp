from flask import Flask, request, jsonify
from models.modules.ConvertToNumber import ConvertToNumber  # 既存の処理を利用

app = Flask(__name__)

@app.route('/sudoku/generate', methods=['POST'])
def generate_sudoku():
    data = request.json
    # ここで既存のSudoku処理を呼び出し
    board = data['board']  # JSONから盤面情報を取得
    converted_board = ConvertToNumber(board)  # 符号化処理を呼び出し
    # 結果をJSONで返す
    return jsonify({"converted_board": converted_board})

if __name__ == '__main__':
    app.run(debug=True)
