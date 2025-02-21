from flask import Flask, render_template, request, jsonify, redirect, url_for
from models.main import generate_sudoku  # models フォルダ内の main.py からインポート

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

    # generate_sudoku 関数に board を渡して結果を受け取る
    result = generate_sudoku(board)

    # 結果をリダイレクトで渡す
    result_message = "数独の解決結果: " + str(result)  # 結果のメッセージを作成
    return redirect(url_for('result', result_message=result_message))

@app.route('/result')
def result():
    # リダイレクトで渡されたメッセージを取得
    result_message = request.args.get('result_message', '結果がありません。')
    
    # 結果をページに表示
    return render_template('result.html', result_message=result_message)

if __name__ == '__main__':
    app.run(debug=True)
