async function analyze() {
  const text = document.getElementById('news-input').value.trim();
  const btn = document.getElementById('analyze-btn');
  const resultCard = document.getElementById('result-card');
  const errorCard = document.getElementById('error-card');

  resultCard.style.display = 'none';
  errorCard.style.display = 'none';

  if (!text) {
    showError('Please enter a news article or headline.');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Analyzing...';

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || 'Something went wrong.');
      return;
    }

    showResult(data);
  } catch (err) {
    showError('Could not connect to the server. Make sure the app is running.');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Analyze';
  }
}

function showResult(data) {
  const resultCard = document.getElementById('result-card');
  const icon = document.getElementById('result-icon');
  const label = document.getElementById('result-label');
  const bar = document.getElementById('confidence-bar');
  const confText = document.getElementById('confidence-text');

  const isFake = data.label === 'FAKE';
  const confidence = data.confidence ? Math.round(data.confidence * 100) : null;

  icon.textContent = isFake ? '🚨' : '✅';
  label.textContent = isFake ? 'FAKE' : 'REAL';
  label.className = `result-label ${isFake ? 'fake' : 'real'}`;

  bar.className = `confidence-bar ${isFake ? 'fake' : 'real'}`;
  bar.style.width = '0%';

  if (confidence !== null) {
    confText.textContent = `Confidence: ${confidence}%`;
    setTimeout(() => { bar.style.width = `${confidence}%`; }, 50);
  } else {
    confText.textContent = '';
    bar.style.width = '0%';
  }

  resultCard.style.display = 'block';
}

function showError(message) {
  const errorCard = document.getElementById('error-card');
  errorCard.textContent = message;
  errorCard.style.display = 'block';
}

document.getElementById('news-input').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && e.ctrlKey) analyze();
});
