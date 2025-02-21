// Sudokuの盤面生成関数
function generateBoard(size) {
  const sudokuForm = document.getElementById('sudokuForm');
  const sudokuBoard = document.getElementById('sudokuBoard');
  const boardTitle = document.getElementById('boardTitle');

  // 盤面をリセット
  sudokuBoard.innerHTML = '';

  // 盤面サイズに合わせたタイトルの表示
  boardTitle.textContent = `${size}×${size}の数独を入力してください`;

  // サイズに応じた入力フィールドを生成
  for (let i = 0; i < size; i++) {
      const row = document.createElement('tr');
      for (let j = 0; j < size; j++) {
          const cell = document.createElement('td');
          const input = document.createElement('input');
          input.type = 'text';
          input.maxLength = '1';  // 各セルには1文字しか入力できない
          input.size = '1';
          cell.appendChild(input);
          row.appendChild(cell);
      }
      sudokuBoard.appendChild(row);
  }

  // フォームの表示
  sudokuForm.style.display = 'block';
}
