from flask import Flask, jsonify, request
import time
import random

from models.ConvertToNumber import ConvertToNumber
from models.Validation import Validation
from models.AddHintToLineSymmetry import AddHintToLineSymmetry
from models.UnifiedNumberOfHints import UnifiedNumberOfHints
from models.generateUniqueSolution import generateUniqueSolution
from models.generateSolutionBoardA import generateSolutionBoardA
from models.printBoard import printBoard

app = Flask(__name__)


@app.route("/generate_sudoku", methods=["POST"])
def generate_sudoku(board):
    # リクエストからJSONデータを取得
    data = request.get_json()

    # JSONデータが正しいか確認
    if not data or 'input' not in data:
        return jsonify({"error": "No input data received"}), 400

    # boardデータとsizeを取得
    input_data = data['input']
    size = int(input_data['size'])
    board = input_data['board']

    print("サイズ")
    print(size)
    print("ボード")
    print(board)

    # 盤面内の空データを文字列の "0" に変換する
    for i in range(size):
        for j in range(size):
            if board[i][j] == '' or board[i][j] is None:
                board[i][j] = '0'

    print("空データを'0'に変換後のボード")
    print(board)

    # デフォルト値と設定を取得
    defaultValue = data.get('defaultValue', 0)
    AddHintToLineTarget = data.get('AddHintToLineTarget', 0)
    LIMIT_TIME = data.get('LIMIT_TIME', 6000000000000000000)

    # 最大解数とターゲットヒント数を設定
    if size == 9:
        MAX_SOLUTIONS = 10
        TARGET_HINT_COUNT = 16
    elif size == 16:
        MAX_SOLUTIONS = 300
        TARGET_HINT_COUNT = 51
    elif size == 25:
        MAX_SOLUTIONS = 20
        TARGET_HINT_COUNT = 250
    else:
        MAX_SOLUTIONS = 10
        TARGET_HINT_COUNT = 20

    # 盤面の文字を数値に変換
    converter = ConvertToNumber(board, size)
    dataConvertedToNumbers = converter.getConvertedData()

    print("数字へ変換後のデータ")
    print(dataConvertedToNumbers)

    # Validationクラスを使用して入力ファイルの正当性チェック
    validator = Validation(
        dataConvertedToNumbers['charToNumberMap'], dataConvertedToNumbers['boardConvertedToNumber'], size)
    if not validator.check():
        return jsonify({"error": "バリデーション失敗"}), 400

    # generateSolutionBoard関数を使用して解盤面Aを取得
    boardA = [row[:]
              for row in dataConvertedToNumbers['boardConvertedToNumber']]
    isSolutionGenerated = generateSolutionBoardA(boardA)
    if not isSolutionGenerated:
        return jsonify({"error": "解盤面Aの生成に失敗しました"}), 400

    # AddHintToLineTarget に応じて処理を分岐
    if AddHintToLineTarget == 1:
        symmetryAdder = AddHintToLineSymmetry(
            dataConvertedToNumbers['boardConvertedToNumber'], boardA)
        symmetricBoards = symmetryAdder.getSymmetricBoards()
        symmetryTypes = ["horizontal", "vertical",
                         "diagonal_up", "diagonal_down"]

        # ヒント数の統一処理
        hintUnifier = UnifiedNumberOfHints(
            symmetricBoards, boardA, targetHintCount=TARGET_HINT_COUNT)
        unifiedBoards = hintUnifier.unifyHints()

        # 最初の選択は最初の盤面を使用
        selectedBoard = unifiedBoards[0]
        selectedBoardName = f"{symmetryTypes[0]}Symmetry"

    else:
        # ランダムにヒントを追加
        selectedBoard = [[0 for _ in range(size)] for _ in range(size)]
        positions = [(i, j) for i in range(size) for j in range(size)]
        random.shuffle(positions)

        # 入力盤面のヒントを追加
        hints_added = 0
        for i in range(size):
            for j in range(size):
                if dataConvertedToNumbers['boardConvertedToNumber'][i][j] != 0:
                    selectedBoard[i][j] = dataConvertedToNumbers['boardConvertedToNumber'][i][j]
                    hints_added += 1

        # 残りのヒントをランダムに追加
        for pos in positions:
            if hints_added >= TARGET_HINT_COUNT:
                break
            i, j = pos
            if selectedBoard[i][j] == 0:
                selectedBoard[i][j] = boardA[i][j]
                hints_added += 1

        selectedBoardName = "Random Hints"

    # 唯一解の生成
    startTime = time.time()
    problemExample, uniqueSolution, numberOfHintsAdded, solutionsPerIteration, timePerHint, addedHintInformation = generateUniqueSolution(
        selectedBoard, MAX_SOLUTIONS, LIMIT_TIME)
    print("生成終わり")
    endTime = time.time()

    generationTime = endTime - startTime
    print(f"生成時間: {generationTime:.2f}秒")

    if uniqueSolution:
        print("\n******************************************")
        print("唯一解を持つ問題例(数字):")
        print("******************************************")
        printBoard(problemExample)

        print("\n******************************************")
        print("その問題例の解答(数字):")
        print("******************************************")
        printBoard(uniqueSolution)

        # 数値から文字に変換して表示
        print("\n******************************************")
        print("文字に変換された問題例(文字):")
        print("******************************************")
        problemBoard = converter.convertBack(problemExample)
        printBoard(problemBoard)

        print("\n******************************************")
        print("文字に変換された解答(文字):")
        print("******************************************")
        solutionBoard = converter.convertBack(uniqueSolution)
        printBoard(solutionBoard)


        # 結果をJSONで返す
        result = {
            "problemBoard": problemBoard,
            "solutionBoard": solutionBoard,
            "generationTime": round(endTime - startTime, 2)
        }
        return jsonify(result)

    else:
        return jsonify({"error": "唯一解の生成に失敗しました"}), 400


if __name__ == "__main__":
    app.run(debug=True)
