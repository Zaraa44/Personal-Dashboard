document.querySelectorAll(".theme-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const theme = btn.dataset.theme;

    if (theme === "sunset") {
      document.documentElement.style.setProperty("--primary", "#ea7e6d");
      document.documentElement.style.setProperty("--primary-light", "#f3a683");
      document.documentElement.style.setProperty("--cpu-gradient", "linear-gradient(90deg,#8a4242,#ff7676)");
      document.documentElement.style.setProperty("--ram-gradient", "linear-gradient(90deg,#9b5449,#ff9a76)");
      document.documentElement.style.setProperty("--disk-gradient", "linear-gradient(90deg,#a96851,#ffbf76)");
    }

    if (theme === "ocean") {
      document.documentElement.style.setProperty("--primary", "#3a7bd5");
      document.documentElement.style.setProperty("--primary-light", "#00d2ff");
      document.documentElement.style.setProperty("--cpu-gradient", "linear-gradient(90deg,#005c97,#363795)");
      document.documentElement.style.setProperty("--ram-gradient", "linear-gradient(90deg,#2193b0,#6dd5ed)");
      document.documentElement.style.setProperty("--disk-gradient", "linear-gradient(90deg,#0f2027,#2c5364)");
    }

    if (theme === "forest") {
      document.documentElement.style.setProperty("--primary", "#11998e");
      document.documentElement.style.setProperty("--primary-light", "#38ef7d");
      document.documentElement.style.setProperty("--cpu-gradient", "linear-gradient(90deg,#355c3a,#6ab04c)");
      document.documentElement.style.setProperty("--ram-gradient", "linear-gradient(90deg,#0f9b0f,#00b09b)");
      document.documentElement.style.setProperty("--disk-gradient", "linear-gradient(90deg,#3ca55c,#b5ac49)");
    }
  });
});
