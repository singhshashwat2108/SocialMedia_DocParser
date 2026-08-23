const UPLOAD_ENDPOINT = '/documents/upload';
const ANALYZE_ENDPOINT = '/analyze';

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const ALLOWED_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png', '.webp'];

const screens = {
  upload: document.getElementById('screen-upload'),
  loading: document.getElementById('screen-loading'),
  error: document.getElementById('screen-error'),
  results: document.getElementById('screen-results'),
};

function showScreen(name) {
  Object.values(screens).forEach((el) => { el.hidden = true; });
  screens[name].hidden = false;
}

const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const fileChosen = document.getElementById('file-chosen');
const fileChosenName = document.getElementById('file-chosen-name');
const uploadError = document.getElementById('upload-error');
const btnAnalyze = document.getElementById('btn-analyze');
const btnClear = document.getElementById('btn-clear');
const btnRetry = document.getElementById('btn-retry');
const btnReset = document.getElementById('btn-reset');
const btnCopy = document.getElementById('btn-copy');
const errorMessageEl = document.getElementById('error-message');

const step1 = document.getElementById('step-1');
const step2 = document.getElementById('step-2');
const step3 = document.getElementById('step-3');

let selectedFile = null;

function extensionOf(filename) {
  const idx = filename.lastIndexOf('.');
  return idx === -1 ? '' : filename.slice(idx).toLowerCase();
}

function showUploadError(message) {
  uploadError.textContent = message;
  uploadError.hidden = false;
}

function clearUploadError() {
  uploadError.hidden = true;
  uploadError.textContent = '';
}

function resetFileSelection() {
  selectedFile = null;
  fileInput.value = '';
  fileChosen.hidden = true;
  btnAnalyze.disabled = true;
}

function setFile(file) {
  clearUploadError();

  if (!ALLOWED_EXTENSIONS.includes(extensionOf(file.name))) {
    resetFileSelection();
    showUploadError('Unsupported file type. Please upload a PDF, JPG, PNG, or WEBP file.');
    return;
  }

  if (file.size > MAX_FILE_SIZE) {
    resetFileSelection();
    showUploadError('File is too large. Maximum size is 10MB.');
    return;
  }

  selectedFile = file;
  fileChosenName.textContent = file.name;
  fileChosen.hidden = false;
  btnAnalyze.disabled = false;
}

dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    fileInput.click();
  }
});

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
  dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) setFile(file);
});

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});

btnClear.addEventListener('click', () => {
  resetFileSelection();
  clearUploadError();
});

function setStep(stepEl, state) {
  stepEl.classList.remove('step-active', 'step-done');
  if (state) stepEl.classList.add(state);
}

function resetSteps() {
  [step1, step2, step3].forEach((s) => setStep(s, null));
}

async function extractErrorMessage(response) {
  try {
    const body = await response.json();
    return body.detail || body.error || `Request failed with status ${response.status}`;
  } catch (_err) {
    return `Request failed with status ${response.status}`;
  }
}

async function runAnalysis() {
  if (!selectedFile) return;

  showScreen('loading');
  resetSteps();
  setStep(step1, 'step-active');

  try {
    const formData = new FormData();
    formData.append('file', selectedFile);

    const uploadResponse = await fetch(UPLOAD_ENDPOINT, {
      method: 'POST',
      body: formData,
    });

    if (!uploadResponse.ok) {
      throw new Error(await extractErrorMessage(uploadResponse));
    }

    setStep(step1, 'step-done');
    setStep(step2, 'step-active');

    const uploadData = await uploadResponse.json();
    const extractedText = uploadData.text || '';

    setStep(step2, 'step-done');
    setStep(step3, 'step-active');

    const analyzeResponse = await fetch(ANALYZE_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: extractedText }),
    });

    if (!analyzeResponse.ok) {
      throw new Error(await extractErrorMessage(analyzeResponse));
    }

    const analysis = await analyzeResponse.json();
    setStep(step3, 'step-done');

    renderResults(extractedText, analysis);
    showScreen('results');
  } catch (err) {
    errorMessageEl.textContent = 'Something went wrong. Try again.';
    showScreen('error');
  }
}

function renderResults(text, analysis) {
  document.getElementById('result-text').textContent = text.trim() || '(No text extracted)';
  document.getElementById('result-score').textContent = analysis.engagement_score ?? '–';
  document.getElementById('result-tone').textContent = analysis.tone || '–';

  const list = document.getElementById('result-suggestions');
  list.innerHTML = '';
  (analysis.suggestions || []).forEach((suggestion) => {
    const li = document.createElement('li');
    li.textContent = suggestion;
    list.appendChild(li);
  });

  document.getElementById('result-improved').textContent = analysis.improved_version || '';
}

btnAnalyze.addEventListener('click', runAnalysis);
btnRetry.addEventListener('click', runAnalysis);

btnCopy.addEventListener('click', () => {
  const text = document.getElementById('result-improved').textContent;
  navigator.clipboard.writeText(text).then(() => {
    const original = btnCopy.textContent;
    btnCopy.textContent = 'Copied!';
    setTimeout(() => { btnCopy.textContent = original; }, 1500);
  });
});

btnReset.addEventListener('click', () => {
  resetFileSelection();
  clearUploadError();
  showScreen('upload');
});

showScreen('upload');
