
document.addEventListener('DOMContentLoaded', function () {

  // ========== 定数定義 ==========
  const form = document.getElementById("manualForm");
  const actionInput = document.getElementById("manualAction");
  const modal     = document.getElementById('manualModal');
  const reopenModal = document.body.dataset.reopenModal === "True";
  const backdrop  = document.getElementById('manualBackdrop');
  const openBtn   = document.getElementById('openManualBtn');
  const returnBtn = document.getElementById('returnManualBtn');
  const saveBtn = document.getElementById("saveManualBtn");
  const updateBtn = document.getElementById("updateWordsCountBtn");
  const hasCsv = document.body.dataset.hasCsv === "true";
  const errBox = document.getElementById("manualErrBox");

  // openBtn / modal / backdrop の存在確認
  if (!openBtn || !modal || !backdrop) {
    console.warn('[modal] 必須要素であるopenBtn / modal / backdrop のいずれかが見つかりません。IDを確認してください。');
    return;
  }

  // ========== モーダル関連の関数 ==========
  // モーダルを開く
  function openModal() {
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
  }

  // モーダルを閉じる
  function closeModal() {
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
  }

  // 元画面にリダイレクトする
  function redirectPreviousPage() {
    if (returnBtn && returnBtn.form) {
      // 戻るボタン押下するとreturnBtnが含まれるフォームのactionのURLを取得
      const actionUrl = returnBtn.form.getAttribute('action')

      // 取得したURLの画面に遷移する
      window.location.href = actionUrl;
    }
  }

  // ========== 入力チェック ==========
  function validateForm() {
    const genre = document.getElementById('genre').value.trim();
    const words = Array.form(document.getElementByName('words'))
                       .map(w => w.value.trim())
                       .filter(Boolean);

    if (!genre) return "ジャンルが入力されていません。"
    if (words.length === 0 ) return "ことばが1つも入力されていません。"
    return "";  // エラーなし
  }


  // ========== アクション選択 ==========
function chooseSaveUpdateValue(btnName, actionValue) {
  btnName.addEventListener("click", () => {
      actionInput.value = actionValue
    });
}
chooseSaveUpdateValue(saveBtn, "manual_save")
chooseSaveUpdateValue(updateBtn, "update_words_count")

  // ========== イベントリスナー登録 ==========
  // モーダルを開く
  if (openBtn) openBtn.addEventListener('click', openModal);

  // モーダルを再度開く
  if (reopenModal) openModal();

  // 背景クリック → モーダルを閉じる
  if (backdrop) backdrop.addEventListener('click', closeModal);

  // Escapeキークリック → モーダルを閉じる
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.style.display !== 'none') closeModal();
  });

  // 戻るボタンクリック → 元の画面にリダイレクト
  if (returnBtn) returnBtn.addEventListener('click', redirectPreviousPage);


  // ========== フォーム送信 ==========
  if (form) {
    form.addEventListener("submit", (event) => {
      // 保存ボタンクリック ⇒ CSVファイルデータを保存
      if (actionInput.value === "manual_save") {
        const errMsg = validateForm();

        if (errMsg) {
          event.preventDefault();   // サーバー送信を止める
          if (errBox) {
            errBox.textContent = errMsg;
            errBox.style.display = "block";
          }
          return;   // 入力エラーがあればここで終了
        }

        if (hasCsv && confirm("CSVファイルの情報を更新します。よろしいですか？")) {
          event.preventDefault(); // キャンセル時は送信しない
           return;
        }
      }
    });
  }
});
