async function fetchEvents() {
  const res = await fetch("/api/google/events");
  if (!res.ok) {
    document.getElementById("google-content").style.display = "none";
    document.getElementById("google-login").style.display = "block";
    return;
  }

  const data = await res.json();
  document.getElementById("google-login").style.display = "none";
  document.getElementById("google-content").style.display = "block";

  const events = data.items || [];
  document.getElementById("google-events").innerHTML = events.map(e => `
    <div>
      <b>${e.summary || "Geen titel"}</b><br>
      ${e.start?.dateTime || e.start?.date || "Onbekend tijdstip"}
    </div>
  `).join("<hr>");
}

fetchEvents();
