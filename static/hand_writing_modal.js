//単純にコピペしただけ。内容を確認すること！！


document.addEventListener('DOMContentLoaded', function () {
  const openBtn   = document.getElementById('openManualBtn');
  const modal     = document.getElementById('manualModal');
  const backdrop  = document.getElementById('manualBackdrop');
  const returnBtn = document.getElementById('returnManualBtn');

  if (!openBtn || !modal || !backdrop) {
    console.warn('[modal] 必須要素が見つかりません。IDを確認してください。');
    return;
  }

  // モーダルを開く
  function openModal() {
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
    const firstInput = modal.querySelector('input, button, textarea, select');
    if (firstInput) firstInput.focus();
  }

  // モーダルを閉じる
  function closeModal() {
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
  }

  // 元画面にリダイレクト
  function redirectPreviousPage() {
    const returnBtn = document.getElementById('returnManualBtn');

    if (returnBtn && returnBtn.form) {
      // 戻るボタン押下するとreturnBtnが含まれるフォームのactionのURLを取得
      const actionUrl = returnBtn.form.getAttribute('action')

      // 取得したURLの画面に遷移する
      window.location.href = actionUrl;
    }
  }

  //*********************************************************************
  // モーダルを開く
  openBtn.addEventListener('click', openModal);

  // 背景クリック → モーダルを閉じる
  backdrop.addEventListener('click', closeModal);

  // 戻るボタンクリック → 元の画面にリダイレクト
  if (returnBtn) {
    returnBtn.addEventListener('click', redirectPreviousPage);
  }

  // Escapeキークリック → モーダルを閉じる
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.style.display !== 'none') closeModal();
  });
});

//更新した内容をCSVファイルに反映する
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("manualForm");
  const saveBtn = document.getElementById("saveManualBtn");
  const hasCsv = document.body.dataset.hasCsv === "true";

  if (form && saveBtn) {
    form.addEventListener("submit", function (event) {
      // 入力チェック
      const genre = document.getElementById("genre").value.trim();
      const words = Array.from(document.getElementsByName("words"))
                        .map(w => w.value.trim())
                        .filter(Boolean);

      let errMsg = "";
      if (!genre) {
        errMsg = "ジャンルが入力されていません。"
      } else if (words.length === 0 ) {
        errMsg = "ことばが1つも入力されていません。"
      }

      if (errMsg) {
        event.preventDefault();   // サーバー送信を止める
        const errBox = document.getElementById("manualErrBox");
        if (errBox) {
          errBox.textContent = errMsg;
          errBox.style.display = "block";
        }
        return;   // 入力エラーがあればここで終了
      }

      if (hasCsv) {
        const confirmed = confirm("CSVファイルの情報を更新します。よろしいですか？");
        if (!confirmed) {
          event.preventDefault(); // キャンセル時は送信しない
          return;
        }
      }
    });
  }
});
