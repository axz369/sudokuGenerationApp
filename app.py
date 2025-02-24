from flask import Flask, render_template, request, jsonify, Response
from models.main import generate_sudoku
import time
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_sudoku():
    data = request.get_json()

    if not data or 'input' not in data or 'board' not in data['input']:
        return jsonify({"error": "No board data received"}), 400

    board = data['input']['board']
    print("Board:")
    for row in board:
        print(row)

    start_time = time.time()

    # generate_sudoku関数からの結果を取得
    result = generate_sudoku(board)

    # Responseオブジェクトからデータを取り出す
    if isinstance(result, Response):
        # JSONデータを取り出す
        result_dict = json.loads(result.get_data(as_text=True))
        
        # resultから各要素を正しく取り出す
        problem_board = result_dict['problemBoard']    # 生成された問題盤面
        solution_board = result_dict['solutionBoard']  # 解答盤面
        generation_time = result_dict['generationTime'] # 生成時間
        size = result_dict['size']
        
    else:
        return jsonify({"error": "Invalid response from solver"}), 500

    # 結果を辞書型で返す
    result_data = {
        "problemBoard": problem_board,    # 生成された問題盤面を使用
        "solutionBoard": solution_board,
        "generationTime": generation_time,
        "size" : size
    }

    return jsonify(result_data)

if __name__ == '__main__':
    app.run(debug=True)