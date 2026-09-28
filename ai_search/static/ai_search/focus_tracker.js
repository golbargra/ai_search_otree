/*
 * Focus tracking, revision counting, and log accumulation for Task pages.
 * Runs on the client and dumps to hidden fields on submit.
 */
(function () {
  const focusField    = document.getElementById('id_focus_lost');
  const revisionField = document.getElementById('id_n_revisions');
  const queryLogField = document.getElementById('id_query_log');
  const aiLogField    = document.getElementById('id_ai_log');
  const nQueriesField = document.getElementById('id_n_queries');
  const nAiTurnsField = document.getElementById('id_n_ai_turns');

  // ---- Focus / blur tracking ----
  let focusLost = 0;
  window.addEventListener('blur', () => {
    focusLost += 1;
    focusField.value = focusLost;
    if (focusLost >= 3) {
      alert("Please keep this window focused during the task. This is your final warning.");
    }
  });

  // ---- Revision counter (counts how many times any answer field changes) ----
  let revisionCount = 0;
  const answerFields = document.querySelectorAll(
    "input[name^='ans_'], input[name='ans_reviews'], input[name='ans_rating']"
  );
  answerFields.forEach(f => {
    f.addEventListener('change', () => {
      revisionCount += 1;
      revisionField.value = revisionCount;
    });
  });

  // ---- Query & AI log accumulators ----
  // In a production system, use postMessage from the embedded iframes,
  // or a browser extension that captures searches/AI turns and POSTs them.
  // Here we expose global functions the iframes (or a wrapper) can call.
  window._queryLog = [];
  window._aiLog    = [];

  window.logQuery = (text) => {
    window._queryLog.push({ t: Date.now(), q: text });
    queryLogField.value = JSON.stringify(window._queryLog);
    nQueriesField.value = window._queryLog.length;
  };

  window.logAiTurn = (msg) => {
    window._aiLog.push({ t: Date.now(), m: msg });
    aiLogField.value = JSON.stringify(window._aiLog);
    nAiTurnsField.value = window._aiLog.length;
  };

  // Flush before submit so the hidden fields have the latest state.
  document.querySelector('.otree-btn-next').addEventListener('click', () => {
    queryLogField.value = JSON.stringify(window._queryLog);
    aiLogField.value    = JSON.stringify(window._aiLog);
  });
})();
