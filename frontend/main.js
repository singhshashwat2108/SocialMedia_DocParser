/* ── Scroll reveal ── */
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }), { threshold: 0.06 });
document.querySelectorAll('.glass-card').forEach(c => io.observe(c));

/* ── File handling ── */
const fileInput  = document.getElementById('file-input');
const uploadZone = document.getElementById('upload-zone');
const fileInfoEl = document.getElementById('file-info');
const btnProcess = document.getElementById('btn-process');
const pillUpload = document.getElementById('pill-upload');
let currentFile  = null;

const fmt = b => b < 1048576 ? (b/1024).toFixed(1)+' KB' : (b/1048576).toFixed(1)+' MB';

function setFile(f) {
  if (!f) return;
  currentFile = f;
  document.getElementById('file-name').textContent = f.name;
  document.getElementById('file-size').textContent = fmt(f.size);
  fileInfoEl.classList.add('show');
  btnProcess.disabled = false;
  pillUpload.innerHTML = '<span class="pill-dot" style="background:#30D158"></span>Ready';
  pillUpload.className = 'pill pill-done show';
}

fileInput.addEventListener('change', () => { if (fileInput.files[0]) setFile(fileInput.files[0]); });

document.getElementById('btn-remove').addEventListener('click', e => {
  e.stopPropagation();
  currentFile = null;
  fileInput.value = '';
  fileInfoEl.classList.remove('show');
  btnProcess.disabled = true;
  pillUpload.innerHTML = '<span class="pill-dot blink"></span>Waiting';
  pillUpload.className = 'pill pill-wait show';
});

uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragover'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
uploadZone.addEventListener('drop', e => {
  e.preventDefault();
  uploadZone.classList.remove('dragover');
  const f = e.dataTransfer.files[0];
  if (f) { fileInput.files = e.dataTransfer.files; setFile(f); }
});

/* ── Progress ── */
function runProgress(label, cb) {
  const wrap = document.getElementById('prog-wrap');
  const fill = document.getElementById('prog-fill');
  const lbl  = document.getElementById('prog-label');
  const pct  = document.getElementById('prog-pct');
  lbl.textContent = label;
  wrap.classList.add('show');
  fill.style.width = '0%';
  let v = 0;
  const iv = setInterval(() => {
    v += Math.random() * 11 + 5;
    if (v >= 100) { v = 100; clearInterval(iv); setTimeout(() => { wrap.classList.remove('show'); cb(); }, 260); }
    fill.style.width = v + '%';
    pct.textContent = Math.round(v) + '%';
  }, 100);
}

/* ── Demo content ── */
const sumHL = 'Generative AI could automate 60–70% of knowledge work tasks. Workers who adapt see 37% productivity gains — making adaptation the defining organizational choice of this decade.';

const summary = `The document examines how artificial intelligence is transforming knowledge work across industries.

• Large language models are automating tasks in research synthesis, legal discovery, financial analysis, and medical literature review — areas long considered exclusively human.

• Productivity gains for AI-augmented workers average 37%, while many organizations still lack formal adoption strategies.

• AI will not eliminate knowledge worker roles wholesale; it automates specific tasks within roles, requiring workers to evolve toward oversight, judgment, and curation.

• The most effective organizational response is redesigning roles around AI collaboration — editors, analysts, and lawyers who govern AI outputs rather than compete with them.

• Companies that invest in broad AI literacy will compound competitive advantages; those treating AI as a niche IT concern risk structural disadvantage within the decade.`;

const qaAnswers = {
  default: "Based on the document's content, this appears to be a strategic analysis of AI's impact on knowledge work, covering productivity shifts, organizational adaptation, and the redefinition of professional roles in an AI-augmented environment.",
  "what is this document about?": "This document is a strategic analysis examining how artificial intelligence — specifically large language models — is reshaping knowledge work. It covers productivity impacts, displacement risks, and how organizations should restructure roles around AI collaboration.",
  "what are the key conclusions?": "The document concludes that: (1) AI will automate 60–70% of knowledge work tasks but not eliminate jobs wholesale; (2) AI-augmented workers see ~37% productivity gains; (3) organizations should redesign roles around human-AI collaboration rather than treating AI as a threat; (4) companies investing in AI literacy will gain durable competitive advantages.",
  "who is the intended audience?": "The document is aimed at organizational leaders, strategy executives, and HR decision-makers who are navigating workforce transformation in response to generative AI adoption.",
  "list the main data points": "Key data points in the document: \n• 60–70% of knowledge work tasks could be automated by generative AI \n• 37% average productivity increase for AI-augmented workers \n• Industries covered: research, legal, financial analysis, and medical literature review \n• Timeframe: structural disadvantage predicted 'within this decade' for laggards"
};

/* ── Process ── */
btnProcess.addEventListener('click', () => {
  btnProcess.disabled = true;
  const cardSummary = document.getElementById('card-summary');
  const cardQA = document.getElementById('card-qa');
  cardSummary.classList.add('visible');
  document.getElementById('pill-sum-proc').classList.add('show');

  runProgress('Analyzing document layout…', () => {
    document.getElementById('empty-summary').style.display = 'none';
    const hl = document.getElementById('sum-callout');
    document.getElementById('sum-hl').textContent = sumHL;
    hl.classList.add('show');
    const sel = document.getElementById('text-summary');
    sel.textContent = summary;
    sel.classList.add('show');
    document.getElementById('foot-summary').classList.add('show');
    document.getElementById('wc-summary').textContent = summary.trim().split(/\s+/).length + ' words';
    document.getElementById('pill-sum-proc').classList.remove('show');
    document.getElementById('pill-sum-done').classList.add('show');

    setTimeout(() => {
      cardQA.classList.add('visible');
      document.getElementById('qa-locked').style.display = 'none';
      document.getElementById('qa-suggest').style.display = 'flex';
      const qaInput = document.getElementById('qa-input');
      const btnSend = document.getElementById('btn-send');
      qaInput.disabled = false;
      btnSend.disabled = false;
      const pillQA = document.getElementById('pill-qa-ready');
      pillQA.style.display = 'inline-flex';
      cardQA.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 500);
  });
});

/* ── Q&A ── */
const qaMessages = document.getElementById('qa-messages');

function addBubble(text, role) {
  const b = document.createElement('div');
  b.className = 'bubble ' + (role === 'user' ? 'bubble-user' : 'bubble-ai');
  b.textContent = text;
  b.style.opacity = '0';
  b.style.transform = 'translateY(6px)';
  b.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
  qaMessages.appendChild(b);
  requestAnimationFrame(() => { b.style.opacity = '1'; b.style.transform = 'none'; });
  qaMessages.scrollTop = qaMessages.scrollHeight;
  return b;
}

function addTyping() {
  const b = document.createElement('div');
  b.className = 'bubble bubble-ai bubble-typing';
  b.id = 'typing-bubble';
  b.innerHTML = '<span></span><span></span><span></span>';
  qaMessages.appendChild(b);
  qaMessages.scrollTop = qaMessages.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById('typing-bubble');
  if (t) t.remove();
}

function sendQuestion(q) {
  if (!q.trim()) return;
  document.getElementById('qa-suggest').style.display = 'none';
  addBubble(q, 'user');
  addTyping();
  const key = q.toLowerCase().trim();
  const answer = qaAnswers[key] || qaAnswers.default;
  setTimeout(() => {
    removeTyping();
    addBubble(answer, 'ai');
  }, 900 + Math.random() * 600);
}

document.getElementById('btn-send').addEventListener('click', () => {
  const inp = document.getElementById('qa-input');
  const val = inp.value.trim();
  if (!val) return;
  inp.value = '';
  inp.style.height = '';
  sendQuestion(val);
});

document.getElementById('qa-input').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    document.getElementById('btn-send').click();
  }
});

document.getElementById('qa-input').addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

function askChip(el) {
  sendQuestion(el.textContent);
}

/* ── Copy ── */
function copyEl(id, btn) {
  navigator.clipboard.writeText(document.getElementById(id).textContent).then(() => {
    const orig = btn.innerHTML;
    btn.innerHTML = '✓ Copied';
    btn.style.color = '#30D158';
    setTimeout(() => { btn.innerHTML = orig; btn.style.color = ''; }, 1800);
  });
}
