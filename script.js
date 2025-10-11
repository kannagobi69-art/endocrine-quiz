/*
 Final script.js — dynamic quiz logic, review screen, explanations, shuffle handled by converter
 - Loads `questions` (from questions.js)
 - Populates sections dropdown
 - Cleans question text leading numbers
 - Shows circular A/B/C/D badges
 - Stores attempts in localStorage
 - Review Answers accessible from Results (button)
*/

(function(){
  // Defensive
  if (typeof questions === 'undefined' || !Array.isArray(questions)) {
    alert('questions.js not found or invalid. Run csv_to_questions.py to generate questions.js from mcqs.csv.');
    console.error('Missing questions variable.');
    return;
  }

  // DOM refs
  const start = document.getElementById('start');
  const quiz = document.getElementById('quiz');
  const results = document.getElementById('results');
  const review = document.getElementById('review');
  const history = document.getElementById('history');

  const playerNameInput = document.getElementById('playerNameInput');
  const sectionSelect = document.getElementById('sectionSelect');
  const startBtn = document.getElementById('startBtn');
  const viewHistoryBtn = document.getElementById('viewHistoryBtn');

  const playerNameDisplay = document.getElementById('playerNameDisplay');
  const currentSectionDisplay = document.getElementById('currentSectionDisplay');
  const progressFill = document.getElementById('progressFill');
  const progressText = document.getElementById('progressText');
  const scoreDisplay = document.getElementById('scoreDisplay');

  const questionContainer = document.getElementById('questionContainer');
  const nextBtn = document.getElementById('nextBtn');
  const finishBtn = document.getElementById('finishBtn');
  const quitBtn = document.getElementById('quitBtn');

  const resultSummary = document.getElementById('resultSummary');
  const sectionResults = document.getElementById('sectionResults');
  const restartBtn = document.getElementById('restartBtn');
  const reviewBtn = document.getElementById('reviewBtn');
  const homeBtn = document.getElementById('homeBtn');

  const reviewContainer = document.getElementById('reviewContainer');
  const backFromReview = document.getElementById('backFromReview');
  const homeFromReview = document.getElementById('homeFromReview');

  const historyContainer = document.getElementById('historyContainer');
  const backFromHistory = document.getElementById('backFromHistory');
  const clearHistoryBtn = document.getElementById('clearHistoryBtn');

  // General state
  let allSections = [];
  let chosenSection = '';
  let pool = []; // selected questions array
  let index = 0;
  let playerName = 'Student';
  let score = 0;
  let answered = false;
  let attempt = { name:'', section:'', start:0, total:0, correct:0, answers:[] };

  const STORAGE_KEY = 'endocrine_quiz_history_v1';

  // Helpers
  function showScreen(id){
    [start, quiz, results, review, history].forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
  }

  function uniqueSections(){
    const s = new Set();
    questions.forEach(q => s.add(q.section || 'General'));
    return Array.from(s).sort();
  }

  function cleanQuestion(s){
    if(!s) return '';
    s = s.toString().trim();
    s = s.replace(/^\s*(?:q\s*\d+[:\.\)]\s*)/i,'');
    s = s.replace(/^\s*\d+[:\.\)]\s*/,'').trim();
    return s;
  }

  function populateSections(){
    allSections = uniqueSections();
    sectionSelect.innerHTML = '<option value="">All Sections (randomized)</option>';
    allSections.forEach(sec => {
      const opt = document.createElement('option');
      opt.value = sec;
      opt.textContent = sec;
      sectionSelect.appendChild(opt);
    });
  }

  function startQuiz(){
    playerName = (playerNameInput.value || 'Student').trim();
    playerNameDisplay.textContent = playerName;
    chosenSection = sectionSelect.value;
    currentSectionDisplay.textContent = chosenSection || 'All Sections';
    // build pool
    if(chosenSection) pool = questions.filter(q => q.section === chosenSection);
    else pool = questions.slice();
    if(pool.length === 0){
      alert('No questions found for that section.');
      return;
    }
    shuffleArray(pool);
    index = 0;
    score = 0;
    answered = false;
    attempt = { name: playerName, section: chosenSection || 'All Sections', start: Date.now(), total: pool.length, correct:0, answers: [] };
    updateScore();
    showScreen('quiz');
    loadQuestion();
  }

  function shuffleArray(arr){
    for(let i = arr.length-1;i>0;i--){
      const j = Math.floor(Math.random()*(i+1));
      [arr[i],arr[j]] = [arr[j],arr[i]];
    }
  }

  function loadQuestion(){
    if(index >= pool.length){
      finishQuiz();
      return;
    }
    answered = false;
    const q = pool[index];
    const qText = cleanQuestion(q.question || '');
    // progress
    progressText.textContent = `${index+1} / ${pool.length}`;
    const pct = Math.round(((index)/pool.length)*100);
    progressFill.style.width = `${pct}%`;
    // build options rows
    const optKeys = ['A','B','C','D'];
    const optionsHTML = optKeys.map(k => {
      const val = (q.options && q.options[k])? q.options[k] : '';
      const badgeClass = k==='A' ? 'badge-a' : (k==='B' ? 'badge-b' : (k==='C' ? 'badge-c' : 'badge-d'));
      return `
        <div class="option-row" data-choice="${k}">
          <div class="option-badge ${badgeClass}">${k}</div>
          <div class="option-text">${val}</div>
        </div>
      `;
    }).join('');
    questionContainer.innerHTML = `<div class="question-area"><h3>Q${index+1}. ${qText}</h3><div class="options">${optionsHTML}</div>
      <div id="feedback" class="feedback" style="display:none;"></div>
      <div id="explain" class="explanation" style="display:none;"></div>
    </div>`;
    Array.from(questionContainer.querySelectorAll('.option-row')).forEach(row => {
      row.addEventListener('click', () => {
        if(answered) return;
        handleChoice(row.getAttribute('data-choice'));
      });
    });
    nextBtn.disabled = true;
    finishBtn.disabled = true;
    nextBtn.style.display = (index < pool.length-1) ? 'inline-block' : 'none';
    finishBtn.style.display = (index === pool.length-1) ? 'inline-block' : 'none';
  }

  function handleChoice(choice){
    answered = true;
    const q = pool[index];
    const correct = (q.correct || 'A').toUpperCase();
    const options = Array.from(questionContainer.querySelectorAll('.option-row'));
    options.forEach(row => row.classList.add('disabled'));
    const correctRow = questionContainer.querySelector(`.option-row[data-choice="${correct}"]`);
    if(correctRow) correctRow.classList.add('correct');
    if(choice !== correct){
      const chosenRow = questionContainer.querySelector(`.option-row[data-choice="${choice}"]`);
      if(chosenRow) chosenRow.classList.add('wrong');
    } else {
      score += 1;
      attempt.correct += 1;
    }
    const chosenText = (q.options && q.options[choice])? q.options[choice] : '';
    attempt.answers.push({
      id: q.id,
      question: cleanQuestion(q.question || ''),
      options: q.options,
      chosenKey: choice,
      chosenText: q.options ? q.options[choice] : '',
      correctKey: correct,
      correctText: q.options ? q.options[correct] : '',
      explanation: q.explanation || ''
    });
    const explan = q.explanation && q.explanation.trim();
    if(explan){
      const explDiv = document.getElementById('explain');
      explDiv.textContent = explan;
      explDiv.style.display = 'block';
    }
    const fb = document.getElementById('feedback');
    fb.textContent = (choice===correct) ? 'Correct ✅' : `Incorrect ❌ — Correct: ${correct}`;
    fb.style.display = 'block';
    fb.style.color = (choice===correct)? '#28a745' : '#dc3545';
    updateScore();
    if(index < pool.length-1) nextBtn.disabled = false;
    else finishBtn.disabled = false;
  }

  function updateScore(){
    scoreDisplay.textContent = score;
  }

  function nextQuestion(){
    index++;
    loadQuestion();
  }

  function finishQuiz(){
    const total = pool.length;
    const correct = attempt.correct;
    const percent = total? Math.round((correct/total)*100):0;
    resultSummary.innerHTML = `<p><strong>${attempt.name}</strong></p>
      <p>Section: <strong>${attempt.section}</strong></p>
      <p>Score: <strong>${correct} / ${total}</strong> (${percent}%)</p>`;
    saveAttempt({
      name: attempt.name,
      section: attempt.section,
      total: attempt.total,
      correct: attempt.correct,
      percent,
      timestamp: Date.now(),
      answers: attempt.answers
    });
    showScreen('results');
  }

  function reviewAnswers(){
    reviewContainer.innerHTML = '';
    attempt.answers.forEach((a, i) => {
      const item = document.createElement('div');
      item.className = 'review-item';
      const qHtml = `<div class="q">Q${i+1}. ${a.question}</div>`;
      const optKeys = ['A','B','C','D'];
      const optionsHtml = optKeys.map(letter => {
        const isCorrect = a.correctKey === letter;
        const isChosen = a.chosenKey === letter;
        const badgeClass = letter === 'A' ? 'badge-a' :
                           letter === 'B' ? 'badge-b' :
                           letter === 'C' ? 'badge-c' : 'badge-d';
        let extraClass = '';
        if (isCorrect) extraClass = 'correct';
        else if (isChosen && !isCorrect) extraClass = 'wrong';
        return `
          <div class="option-row ${extraClass}" style="padding:8px 10px;">
            <div class="option-badge ${badgeClass}" style="width:38px;height:38px;font-size:16px">${letter}</div>
            <div class="option-text">${a.options ? a.options[letter] || '' : ''}</div>
          </div>`;
      }).join('');
      const explainHtml = `<div class="explain">${a.explanation || '<em>No explanation provided.</em>'}</div>`;
      item.innerHTML = qHtml + `<div class="options">${optionsHtml}</div>` + explainHtml;
      reviewContainer.appendChild(item);
    });
    showScreen('review');
  }

  // History
  function loadHistory(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch(e){ return []; }
  }

  function saveAttempt(obj){
    const hist = loadHistory();
    hist.unshift(obj);
    if(hist.length > 300) hist.length = 300;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(hist));
  }

  function showHistory(){
    const hist = loadHistory();
    if(!hist || hist.length === 0){
      historyContainer.innerHTML = '<div class="small">No attempts yet.</div>';
    } else {
      historyContainer.innerHTML = hist.map(h => {
        const d = new Date(h.timestamp).toLocaleString();
        return `<div class="history-item">
          <div><div style="font-weight:700">${h.name}</div><div class="meta">${h.section} • ${d}</div></div>
          <div style="text-align:right"><div style="font-weight:700">${h.percent}%</div><div class="meta">${h.correct}/${h.total}</div></div>
        </div>`;
      }).join('');
    }
    showScreen('history');
  }

  function clearHistory(){
    if(!confirm('Clear all history?')) return;
    localStorage.removeItem(STORAGE_KEY);
    showHistory();
  }

  // Button wiring
  startBtn.addEventListener('click', startQuiz);
  viewHistoryBtn.addEventListener('click', showHistory);
  nextBtn.addEventListener('click', nextQuestion);
  finishBtn.addEventListener('click', finishQuiz);
  quitBtn.addEventListener('click', ()=> showScreen('start'));
  restartBtn.addEventListener('click', startQuiz);
  reviewBtn.addEventListener('click', reviewAnswers);
  homeBtn.addEventListener('click', ()=> showScreen('start'));
  backFromReview.addEventListener('click', ()=> showScreen('results'));
  homeFromReview.addEventListener('click', ()=> showScreen('start'));
  backFromHistory.addEventListener('click', ()=> showScreen('start'));
  clearHistoryBtn.addEventListener('click', clearHistory);

  // Keyboard shortcuts
  document.addEventListener('keydown', (e)=>{
    if(!quiz.classList.contains('active')) return;
    const k = e.key.toUpperCase();
    if(['A','B','C','D'].includes(k)){
      const row = document.querySelector(`.option-row[data-choice="${k}"]`);
      if(row && !row.classList.contains('disabled')) row.click();
    }
    if(e.key === 'Enter'){
      if(answered && !nextBtn.disabled) nextBtn.click();
      if(answered && nextBtn.style.display === 'none' && !finishBtn.disabled) finishBtn.click();
    }
  });

  // Init
  populateSections();
  showScreen('start');
})();
