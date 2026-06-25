/**
 * Hugo Chroma 代码块增强 — render-hook 组件版
 * 功能:复制 / 软折行切换 / 折叠·展开 / 自动折叠
 */

document.addEventListener('DOMContentLoaded', function () {
  /* ── 事件委托:按 data-act 分发 ── */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-act]');
    if (!btn) return;
    var act = btn.getAttribute('data-act');
    var block = btn.closest('.code-block');
    if (!block) return;
    var body = block.querySelector('.code-block__body');
    if (!body) return;

    if (act === 'copy') {
      navigator.clipboard.writeText(body.textContent).then(function () {
        btn.textContent = '已复制';
        setTimeout(function () { btn.textContent = '复制'; }, 1500);
      }).catch(function () {
        btn.textContent = '失败';
        setTimeout(function () { btn.textContent = '复制'; }, 1500);
      });
    }

    if (act === 'wrap') {
      body.classList.toggle('is-wrap');
      btn.textContent = body.classList.contains('is-wrap') ? '取消折行' : '软折行';
    }

    if (act === 'fold') {
      block.classList.toggle('is-folded');
      btn.textContent = block.classList.contains('is-folded') ? '展开' : '折叠';
    }
  });

  /* ── 自动折叠:scrollHeight > 480px 的块默认折叠 ── */
  var FOLD_THRESHOLD = 480;
  document.querySelectorAll('.code-block').forEach(function (block) {
    var body = block.querySelector('.code-block__body');
    if (!body) return;
    if (body.scrollHeight > FOLD_THRESHOLD) {
      block.classList.add('is-folded');
      var foldBtn = block.querySelector('[data-act="fold"]');
      if (foldBtn) foldBtn.textContent = '展开';
    }
  });
});
