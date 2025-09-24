let pomodoroTime = 25 * 60; // 25 minuten in seconden
let timer = null;
let isRunning = false;

const timeDisplay = document.getElementById("pomodoro-time");
const startBtn = document.getElementById("start-pomodoro");
const pauseBtn = document.getElementById("pause-pomodoro");
const resetBtn = document.getElementById("reset-pomodoro");

function updateDisplay() {
  const minutes = Math.floor(pomodoroTime / 60);
  const seconds = pomodoroTime % 60;
  timeDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

function startTimer() {
  if (isRunning) return;
  isRunning = true;
  timer = setInterval(() => {
    if (pomodoroTime > 0) {
      pomodoroTime--;
      updateDisplay();
    } else {
      clearInterval(timer);
      isRunning = false;
      alert("Pomodoro klaar! Tijd voor een pauze 🍅");
    }
  }, 1000);
}

function pauseTimer() {
  clearInterval(timer);
  isRunning = false;
}

function resetTimer() {
  clearInterval(timer);
  isRunning = false;
  pomodoroTime = 25 * 60;
  updateDisplay();
}

// Event listeners
startBtn.addEventListener("click", startTimer);
pauseBtn.addEventListener("click", pauseTimer);
resetBtn.addEventListener("click", resetTimer);

// Init
updateDisplay();
