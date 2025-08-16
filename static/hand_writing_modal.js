//単純にコピペしただけ。内容を確認すること！！


document.addEventListener('DOMContentLoaded', function () {
  const openBtn  = document.getElementById('openManualBtn');
  const modal    = document.getElementById('manualModal');
  const backdrop = document.getElementById('manualBackdrop');
  const closeBtn = document.getElementById('closeManualBtn');

  if (!openBtn || !modal || !backdrop) {
    console.warn('[modal] 必須要素が見つかりません。IDを確認してください。');
    return;
  }

  function openModal() {
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
    const firstInput = modal.querySelector('input, button, textarea, select');
    if (firstInput) firstInput.focus();
  }
  function closeModal() {
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
  }

  openBtn.addEventListener('click', openModal);
  backdrop.addEventListener('click', closeModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.style.display !== 'none') closeModal();
  });
});
