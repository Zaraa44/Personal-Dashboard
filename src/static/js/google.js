async function fetchEvents(limit = 8) {
  const res = await fetch("/api/google/events");
  if (!res.ok) {
    document.getElementById("google-content").style.display = "none";
    document.getElementById("google-login").style.display = "block";
    return;
  }

  const data = await res.json();
  document.getElementById("google-login").style.display = "none";
  document.getElementById("google-content").style.display = "block";

  // Eerstvolgende `limit` events
  const events = (data.items || []).slice(0, limit);

  document.getElementById("google-events").innerHTML = events.map(e => {
    const date = e.start?.dateTime || e.start?.date || "Onbekend";
    const title = e.summary || "Geen titel";

    return `
      <div class="event-card">
        <div class="event-date">${new Date(date).toLocaleDateString("nl-NL", { weekday: "short", day: "numeric", month: "short" })}</div>
        <div class="event-title">${title}</div>
        <div class="event-time">${new Date(date).toLocaleTimeString("nl-NL", { hour: "2-digit", minute: "2-digit" })}</div>
      </div>
    `;
  }).join("");
}

// standaard: 8 events
fetchEvents(8);
