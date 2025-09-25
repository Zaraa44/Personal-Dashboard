

function updateDateTime() {
  const now = new Date();

  // Datum
  const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
  document.getElementById("current-date").textContent = now.toLocaleDateString("nl-NL", options);

  // Tijd
  const time = now.toLocaleTimeString("nl-NL", { hour: "2-digit", minute: "2-digit" });
  document.getElementById("current-time").textContent = time;
}


updateDateTime();
setInterval(updateDateTime, 1000); // klok live

