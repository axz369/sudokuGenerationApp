import time
import json
import random  # ランダムなヒント追加のために追加

from modules.ConvertToNumber import ConvertToNumber
from modules.Validation import Validation
from modules.UnifiedNumberOfHints import UnifiedNumberOfHints
from modules.generateUniqueSolution import generateUniqueSolution

from utility.generateSolutionBoardG import generateSolutionBoardG
from utility.printBoard import printBoard


if __name__ == "__main__":

    #########################################################
    # プログラム設定
    INPUT_FILE = 'input9.json'
    INPUT_KEY = 'input2'

    LIMIT_TIME = 1000

    if '9' in INPUT_FILE:
        MAX_SOLUTIONS = 100
        TARGET_HINT_COUNT = 16
    elif '16' in INPUT_FILE:
        MAX_SOLUTIONS = 300
        TARGET_HINT_COUNT = 51
    elif '25' in INPUT_FILE:
        MAX_SOLUTIONS = 20
        TARGET_HINT_COUNT = 250
    else:
        MAX_SOLUTIONS = 10
        TARGET_HINT_COUNT = 20
    #########################################################

    # JSONファイルを読み込む
    with open(INPUT_FILE, 'r', encoding="utf-8") as file:
        data = json.load(file)

    # 使用する数独の問題を選択
    sudokuProblem = data["inputs"][INPUT_KEY]
    board = sudokuProblem["board"]
    maxNumber = sudokuProblem["maxNumber"]

    # 入力盤面を表示
    print("入力盤面:")
    printBoard(board)

    # 盤面の文字を数値に変換
    converter = ConvertToNumber(board, maxNumber)
    dataConvertedToNumbers = converter.getConvertedData()

    # Validationクラスを使用して入力ファイルの正当性チェック
    validator = Validation(
        dataConvertedToNumbers['charToNumberMap'], dataConvertedToNumbers['boardConvertedToNumber'], maxNumber)
    if not validator.check():
        print("バリデーション失敗")
        exit(1)
    else:
        print("バリデーション成功")

    # generateSolutionBoard関数を使用して解盤面Aを取得
    boardA = [row[:]
              for row in dataConvertedToNumbers['boardConvertedToNumber']]

    isSolutionGenerated = generateSolutionBoardG(boardA)

    if not isSolutionGenerated:
        print("解盤面Aの生成に失敗しました。")
        exit(1)
    else:
        print("解盤面Aが生成されました")
        printBoard(converter.convertBack(boardA))

    
    # 対称性に基づいたヒント追加をスキップし、ランダムにヒントを追加

    selectedBoard = [[0 for _ in range(maxNumber)]
                    for _ in range(maxNumber)]  # 空の盤面を作成
    positions = [(i, j) for i in range(maxNumber)
                for j in range(maxNumber)]
    random.shuffle(positions)

    # 入力盤面のヒントを追加
    hints_added = 0
    for i in range(maxNumber):
        for j in range(maxNumber):
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
    print(f"選ばれた盤面 : {selectedBoardName}")
    printBoard(selectedBoard)

    # 唯一解の生成
    startTime = time.time()

    # 問題例,解盤面,追加したヒントの数,再利用した解盤面数
    problemExample, uniqueSolution, numberOfHintsAdded, solutionsPerIteration, timePerHint, addedHintInformation = generateUniqueSolution(
        selectedBoard, MAX_SOLUTIONS, LIMIT_TIME)
    numberOfGeneratedBoards = solutionsPerIteration  # 変数名を統一
    numberOfReusedSolutions = [0] * \
        len(solutionsPerIteration)

    endTime = time.time()

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
        printBoard(converter.convertBack(problemExample))

        print("\n******************************************")
        print("文字に変換された解答(文字):")
        print("******************************************")
        printBoard(converter.convertBack(uniqueSolution))

    else:
        print("唯一解の生成に失敗しました。")

    generationTime = endTime - startTime
    print(f"生成時間: {generationTime:.2f}秒")

    # 各ステップで生成された解の数と再利用した解の数を表示
print("\n******************************************")
print("各ステップで生成された解の数と再利用した解の数:")
print("******************************************")
for idx, (generated, reused) in enumerate(zip(numberOfGeneratedBoards, numberOfReusedSolutions)):
    if reused > 0:
        print(
            f"ステップ {idx + 1}: {generated} 個の解が生成され、フィルタリング後に {reused} 個の解を再利用しました")
    else:
        print(f"ステップ {idx + 1}: {generated} 個の解が生成されました")

print("\n******************************************")
print("記録用")
print("******************************************")

print()

print("唯一解生成にかかった時間")
print(f"{generationTime:.2f}")



print()
print("ヒント追加回数")
print(f"{numberOfHintsAdded} ", end="")
output_list = []
for i in range(len(numberOfGeneratedBoards)):
    generated = numberOfGeneratedBoards[i]
    reused = numberOfReusedSolutions[i - 1] if i > 0 else 0
    if reused > 0:
        output_list.append(f"{generated}({reused})")
    else:
        output_list.append(f"{generated}")

# 最後の要素が '1' であれば削除
if output_list and output_list[-1] == '1':
    output_list.pop()

print(f"[{', '.join(output_list)}]")



print()
print("追加ヒントごとの時間")
# 小数点第3位まで四捨五入したリストを出力
formatted_times = [f"{round(time, 3)}" for time in timePerHint]
print(", ".join(formatted_times))



print()
print("追加ヒント情報")
number_to_char = {v: k for k, v in dataConvertedToNumbers['charToNumberMap'].items()}
print(",".join(f"({row}, {col}, {number_to_char[num]})" for row, col, num in addedHintInformation))