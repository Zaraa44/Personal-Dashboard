const title = document.getElementById("dashboard-title");
const icon = document.getElementById("fullscreen-icon");

title.addEventListener("click", () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().then(() => {
      document.body.classList.add("fullscreen-mode");
      icon.textContent = "";
    });
  } else {
    document.exitFullscreen().then(() => {
      document.body.classList.remove("fullscreen-mode");
      icon.textContent = "⛶";
    });
  }
});

document.addEventListener("fullscreenchange", () => {
  if (document.fullscreenElement) {
    document.body.classList.add("fullscreen-mode");
    fetchEvents(10);
  } else {
    document.body.classList.remove("fullscreen-mode");
    fetchEvents(8);
  }
});
