let isPlaying = false;

function msToTime(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

async function fetchNowPlaying() {
  try {
    const res = await fetch("/api/spotify/current");
    if (!res.ok) {
      if (res.status === 401) {
        document.getElementById("spotify-content").style.display = "none";
        document.getElementById("spotify-login").style.display = "block";
        return;
      }
      console.error("Fout response van backend:", res.status);
      return;
    }

    const data = await res.json();
    document.getElementById("spotify-login").style.display = "none";
    document.getElementById("spotify-content").style.display = "block";

    if (data.error || !data.name) {
      document.getElementById("track-name").textContent = "Geen muziek afgespeeld";
      isPlaying = false;
      updatePlayButton();
      return;
    }

    document.getElementById("track-name").textContent = data.name;
    document.getElementById("artist-name").textContent = data.artists;
    document.getElementById("album-art").src = data.album_image;

    isPlaying = data.is_playing ?? false;
    updatePlayButton();
  } catch (e) {
    console.error("Geen geldige JSON van backend:", e);
  }
}

async function apiCall(endpoint, method = "POST") {
  try {
    const res = await fetch(`/api/spotify/${endpoint}`, { method });
    return await res.json();
  } catch (err) {
    console.error("Spotify API fout:", err);
  }
}

document.getElementById("play-btn").addEventListener("click", async () => {
  if (isPlaying) {
    await apiCall("pause", "PUT");
    isPlaying = false;
  } else {
    await apiCall("play", "PUT");
    isPlaying = true;
  }
  updatePlayButton();
});

document.getElementById("next-btn").addEventListener("click", () => apiCall("next"));
document.getElementById("prev-btn").addEventListener("click", () => apiCall("previous"));

function updatePlayButton() {
  const btn = document.getElementById("play-btn");
  btn.textContent = isPlaying ? "⏸" : "▶";
}

fetchNowPlaying();
setInterval(fetchNowPlaying, 1000);
