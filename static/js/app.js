const SAMPLES = {
  fake: "BREAKING: Scientists at NASA have confirmed the moon landing was staged in a Hollywood studio by Stanley Kubrick. Leaked government documents reveal officials have been covering up alien contact since 1947. George Soros is secretly funding a globalist agenda to control world governments through microchips hidden in vaccines.",
  real: "WASHINGTON (Reuters) - The U.S. economy added 275,000 jobs in February, the Labor Department said on Friday, beating economists' expectations and signaling continued resilience in the labor market despite the Federal Reserve keeping interest rates at a 23-year high to combat inflation.",
};

function updateWordCount() {
  const text = document.getElementById('news-input').value.trim();
  const words = text ? text.split(/\s+/).length : 0;
  document.getElementById('word-count').textContent = `${words} word${words !== 1 ? 's' : ''}`;
}

function loadSample(type) {
  const ta = document.getElementById('news-input');
  ta.value = SAMPLES[type];
  updateWordCount();
  ta.focus();
}

function clearInput() {
  document.getElementById('news-input').value = '';
  document.getElementById('word-count').textContent = '0 words';
  document.getElementById('result-card').style.display = 'none';
  document.getElementById('error-card').style.display = 'none';
  document.getElementById('news-input').focus();
}

async function analyze() {
  const text = document.getElementById('news-input').value.trim();
  const btn = document.getElementById('analyze-btn');
  const btnText = document.getElementById('btn-text');
  const spinner = document.getElementById('btn-spinner');
  const resultCard = document.getElementById('result-card');
  const errorCard = document.getElementById('error-card');

  resultCard.style.display = 'none';
  errorCard.style.display = 'none';

  if (!text) { showError('Please enter a news article or headline.'); return; }

  btn.disabled = true;
  btnText.textContent = 'Analyzing...';
  spinner.classList.remove('hidden');

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    if (!res.ok) { showError(data.error || 'Something went wrong.'); return; }
    showResult(data);
  } catch {
    showError('Could not connect to the server.');
  } finally {
    btn.disabled = false;
    btnText.textContent = 'Analyze Article';
    spinner.classList.add('hidden');
  }
}

function showResult(data) {
  const isFake = data.label === 'FAKE';
  const confidence = data.confidence ? Math.round(data.confidence * 100) : null;

  document.getElementById('result-glow').className = `result-glow ${isFake ? 'fake' : 'real'}`;
  document.getElementById('result-icon').textContent = isFake ? '🚨' : '✅';

  const label = document.getElementById('result-label');
  label.textContent = isFake ? 'FAKE NEWS' : 'REAL NEWS';
  label.className = `result-label ${isFake ? 'fake' : 'real'}`;

  document.getElementById('result-description').textContent = isFake
    ? 'This article shows strong indicators of misinformation or fabricated content.'
    : 'This article shows strong indicators of credible, factual reporting.';

  const bar = document.getElementById('confidence-bar');
  bar.className = `confidence-bar ${isFake ? 'fake' : 'real'}`;
  bar.style.width = '0%';

  if (confidence !== null) {
    document.getElementById('confidence-pct').textContent = `${confidence}%`;
    setTimeout(() => { bar.style.width = `${confidence}%`; }, 60);
  }

  const card = document.getElementById('result-card');
  card.style.display = 'block';
}

function showError(msg) {
  const el = document.getElementById('error-card');
  el.textContent = `⚠️  ${msg}`;
  el.style.display = 'block';
}

document.getElementById('news-input').addEventListener('keydown', e => {
  if (e.key === 'Enter' && e.ctrlKey) analyze();
});
