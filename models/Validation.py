class Validation:
    def __init__(self, charToNumberMap, board, size):
        self.charToNumberMap = charToNumberMap
        self.board = board
        self.size = size
        self.subBlockSize = int(size ** 0.5)
        self.MAX_RECURSION_DEPTH = 1000
        self.error_messages = []  # エラーメッセージを保存するリスト

    def check(self):
        if not self.checkRows():
            return False
        if not self.checkColumns():
            return False
        if not self.checkBlocks():
            return False
        if not self.checkCharCount():
            return False
        return True

    def getCharFromNumber(self, number):
        for char, num in self.charToNumberMap.items():
            if num == number:
                return char
        return str(number)

    def checkRows(self):
        for i, row in enumerate(self.board):
            values = []
            for j, val in enumerate(row):
                if val != 0:
                    if val in values:
                        char_value = self.getCharFromNumber(val)
                        error_msg = f"Validation失敗 同じ行で重複 : {i+1}行  {j+1}列  に重複した値 '{char_value}' が存在します。"
                        self.error_messages.append(error_msg)
                        print(error_msg)  # ログのために残す
                        return False
                    values.append(val)
        return True

    def checkColumns(self):
        for col in range(self.size):
            values = []
            for row in range(self.size):
                val = self.board[row][col]
                if val != 0:
                    if val in values:
                        char_value = self.getCharFromNumber(val)
                        error_msg = f"Validation失敗 同じ列で重複 : 列 {col+1} 行 {row+1} に重複した値 '{char_value}' が存在します。"
                        self.error_messages.append(error_msg)
                        print(error_msg)
                        return False
                    values.append(val)
        return True

    def checkBlocks(self):
        for block_row in range(self.subBlockSize):
            for block_col in range(self.subBlockSize):
                values = []
                for row in range(self.subBlockSize):
                    for col in range(self.subBlockSize):
                        value = self.board[block_row * self.subBlockSize + row][block_col * self.subBlockSize + col]
                        if value != 0:
                            if value in values:
                                char_value = self.getCharFromNumber(value)
                                error_msg = f"Validation失敗 同じブロックで重複 : ブロック ({block_row+1}, {block_col+1}) 内に重複した値 '{char_value}' が存在します。"
                                self.error_messages.append(error_msg)
                                print(error_msg)
                                return False
                            values.append(value)
        return True

    def checkCharCount(self):
        if len(self.charToNumberMap) > self.size:
            error_msg = f"Validation失敗 : 入力された盤面の文字の種類数 {len(self.charToNumberMap)} が最大値 {self.size} を超えています。"
            self.error_messages.append(error_msg)
            print(error_msg)
            return False
        return True

    def getErrorMessages(self):
        return self.error_messages