from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_sudoku():
    # フロントエンドから送信されたJSONデータを取得
    data = request.get_json()

    # データの検証：ボードが含まれていない場合はエラーレスポンスを返す
    if not data or 'board' not in data:
        return jsonify({"error": "No board data received"}), 400

    # 受け取ったデータを表示
    print("Received Sudoku board data:")
    print(data)

    # ボードのデータを取り出して、必要な処理を実行
    board = data['board']
    print("Board:")
    for row in board:
        print(row)

    # improvementMain.pyのprocess_sudoku関数をインポート
    from models.improvementMain import process_sudoku

    # process_sudoku関数にboardを渡して結果を受け取る
    result = process_sudoku(board)

    # 処理結果をレスポンスとして返す
    return jsonify({"message": "数独データを受け取りました！", "result": result}), 200

@app.route('/result')
def result():
    # リダイレクトで渡されたメッセージを取得
    result_message = request.args.get('result_message', '結果がありません。')
    
    # 結果をページに表示
    return render_template('result.html', result_message=result_message)

if __name__ == '__main__':
    app.run(debug=True)
