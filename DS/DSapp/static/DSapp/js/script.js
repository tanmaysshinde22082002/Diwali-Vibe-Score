document.addEventListener("DOMContentLoaded", () => {
  const scoreElem = document.querySelector(".score-number");
  if (!scoreElem) return;

  const targetScore = parseInt(scoreElem.dataset.score);
  let current = 0;
  const interval = setInterval(() => {
    current++;
    scoreElem.textContent = current;
    if (current >= targetScore) clearInterval(interval);
  }, 15);
});
