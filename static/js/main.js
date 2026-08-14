// ---------------------------------------------------------------------
// Animated stat counters
// ---------------------------------------------------------------------
(function animateCounters() {
  document.querySelectorAll('[data-count]').forEach((el) => {
    const target = parseInt(el.getAttribute('data-count'), 10) || 0;
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = 900;
    const start = performance.now();
    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target) + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
})();

// ---------------------------------------------------------------------
// Animated breakdown bars (profile page)
// ---------------------------------------------------------------------
(function animateBars() {
  document.querySelectorAll('.breakdown-fill').forEach((el, i) => {
    const pct = el.getAttribute('data-pct');
    setTimeout(() => { el.style.width = pct + '%'; }, 150 + i * 90);
  });

  const circle = document.getElementById('score-circle');
  if (circle) {
    const target = circle.getAttribute('data-target');
    setTimeout(() => { circle.style.transition = 'stroke-dashoffset 1.1s cubic-bezier(.2,.8,.2,1)'; circle.style.strokeDashoffset = target; }, 200);
  }
})();

// ---------------------------------------------------------------------
// Drag & drop upload (index page)
// ---------------------------------------------------------------------
(function setupDropzone() {
  const dropzone = document.getElementById('dropzone');
  const input = document.getElementById('resume-input');
  const fileList = document.getElementById('file-list');
  if (!dropzone || !input) return;

  let files = [];

  function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  function render() {
    fileList.innerHTML = '';
    files.forEach((f) => {
      const chip = document.createElement('div');
      chip.className = 'file-chip';
      const ext = f.name.split('.').pop().toUpperCase();
      chip.innerHTML = `<span class="fname">${f.name}</span><span class="fsize">${ext} · ${formatSize(f.size)}</span>`;
      fileList.appendChild(chip);
    });
  }

  function syncInput() {
    const dt = new DataTransfer();
    files.forEach((f) => dt.items.add(f));
    input.files = dt.files;
  }

  dropzone.addEventListener('click', () => input.click());

  ['dragenter', 'dragover'].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
  });
  ['dragleave', 'drop'].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => { e.preventDefault(); dropzone.classList.remove('dragover'); });
  });

  dropzone.addEventListener('drop', (e) => {
    const dropped = Array.from(e.dataTransfer.files);
    files = files.concat(dropped);
    syncInput();
    render();
  });

  input.addEventListener('change', () => {
    files = Array.from(input.files);
    render();
  });
})();

// ---------------------------------------------------------------------
// Processing overlay pipeline animation on submit
// ---------------------------------------------------------------------
(function setupProcessingOverlay() {
  const form = document.getElementById('analyze-form');
  const overlay = document.getElementById('processing-overlay');
  if (!form || !overlay) return;

  form.addEventListener('submit', (e) => {
    const input = document.getElementById('resume-input');
    const jd = document.getElementById('job_description');
    if (!input.files.length || !jd.value.trim()) return; // let native validation handle it

    e.preventDefault();
    overlay.classList.add('active');

    const steps = Array.from(document.querySelectorAll('.step-item'));
    let i = 0;

    function advance() {
      if (i > 0) {
        steps[i - 1].classList.remove('active');
        steps[i - 1].classList.add('done');
        steps[i - 1].querySelector('.step-icon').textContent = '✓';
      }
      if (i < steps.length) {
        steps[i].classList.add('active');
        i++;
        setTimeout(advance, 500);
      } else {
        setTimeout(() => form.submit(), 300);
      }
    }
    advance();
  });
})();

// ---------------------------------------------------------------------
// Interview question category filter (profile page)
// ---------------------------------------------------------------------
(function setupQuestionFilters() {
  const filterBar = document.getElementById('qcat-filters');
  const grid = document.getElementById('question-grid');
  if (!filterBar || !grid) return;

  filterBar.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    filterBar.querySelectorAll('.pill').forEach((p) => p.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.getAttribute('data-cat');
    grid.querySelectorAll('.q-card').forEach((card) => {
      const show = cat === 'all' || card.getAttribute('data-cat') === cat;
      card.style.display = show ? '' : 'none';
    });
  });

  grid.addEventListener('click', (e) => {
    const btn = e.target.closest('.copy-btn');
    if (!btn) return;
    const text = btn.getAttribute('data-question');
    navigator.clipboard?.writeText(text).then(() => {
      const old = btn.textContent;
      btn.textContent = 'Copied ✓';
      setTimeout(() => { btn.textContent = old; }, 1200);
    });
  });

  const exportBtn = document.getElementById('export-questions');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      const cards = Array.from(grid.querySelectorAll('.q-card'));
      const lines = cards.map((c) => {
        const cat = c.getAttribute('data-cat');
        const text = c.querySelector('.q-text').textContent.trim();
        const diff = c.querySelector('.diff-badge').textContent.trim();
        return `[${cat} · ${diff}] ${text}`;
      });
      const blob = new Blob([lines.join('\n\n')], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'interview_questions.txt';
      a.click();
      URL.revokeObjectURL(url);
    });
  }
})();
