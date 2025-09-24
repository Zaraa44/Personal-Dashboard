async function fetchSystem() {
  try {
    const res = await fetch("/api/system/status");
    if (!res.ok) return;

    const data = await res.json();

    // CPU
    document.getElementById("cpu-usage").textContent = data.cpu + "%";
    document.getElementById("cpu-bar").style.width = data.cpu + "%";

    // RAM
    document.getElementById("ram-usage").textContent =
      `${data.memory.used} / ${data.memory.total} GB (${data.memory.percent}%)`;
    document.getElementById("ram-bar").style.width = data.memory.percent + "%";

    // Disk
    document.getElementById("disk-usage").textContent =
      `${data.disk.used} / ${data.disk.total} GB (${data.disk.percent}%)`;
    document.getElementById("disk-bar").style.width = data.disk.percent + "%";

  } catch (err) {
    console.error("System fetch error:", err);
  }
}

fetchSystem();
setInterval(fetchSystem, 3000);
