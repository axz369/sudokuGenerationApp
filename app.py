from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/input9')
def input9():
    return render_template('sudoku_input9.html')

@app.route('/submit', methods=['POST'])
def submit_sudoku():
    data = request.get_json()  # フロントエンドから送信されたJSONデータを取得

    if not data or 'board' not in data:
        return jsonify({"error": "No board data received"}), 400

    # ボードのデータを取り出して、必要な処理を実行
    board = data['board']
    print("Received Sudoku board:")
    for row in board:
        print(row)

    # 数独の解決や検証処理をここで行うことができます。

    # 処理が成功した場合のレスポンス
    return jsonify({"message": "数独データを受け取りました！"}), 200

if __name__ == '__main__':
    app.run(debug=True)
