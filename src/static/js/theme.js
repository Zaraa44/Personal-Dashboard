document.querySelectorAll(".theme-btn").forEach(btn => {
  btn.addEventListener("click", () => {
  const themes = {
  sunset: {
    primary: "#ea7e6d", light: "#f3a683",
    cpu: "linear-gradient(90deg,#8a4242,#ff7676)",
    ram: "linear-gradient(90deg,#9b5449,#ff9a76)",
    disk: "linear-gradient(90deg,#a96851,#ffbf76)"
  },
  ocean: {
    primary: "#3a7bd5", light: "#00d2ff",
    cpu: "linear-gradient(90deg,#005c97,#363795)",
    ram: "linear-gradient(90deg,#2193b0,#6dd5ed)",
    disk: "linear-gradient(90deg,#0f2027,#2c5364)"
  },
  forest: {
    primary: "#11998e", light: "#38ef7d",
    cpu: "linear-gradient(90deg,#355c3a,#6ab04c)",
    ram: "linear-gradient(90deg,#0f9b0f,#00b09b)",
    disk: "linear-gradient(90deg,#3ca55c,#b5ac49)"
  },
  pink: {
    primary: "#ff6ec7", light: "#ffb6f9",
    cpu: "linear-gradient(90deg,#b91d73,#f953c6)",
    ram: "linear-gradient(90deg,#ff758c,#ff7eb3)",
    disk: "linear-gradient(90deg,#f857a6,#ff5858)"
  },
  grey: {
    primary: "#888", light: "#aaa",
    cpu: "linear-gradient(90deg,#555,#999)",
    ram: "linear-gradient(90deg,#666,#bbb)",
    disk: "linear-gradient(90deg,#444,#777)"
  },
  white: {
    primary: "#f5f5f5", light: "#ffffff",
    cpu: "linear-gradient(90deg,#ddd,#fff)",
    ram: "linear-gradient(90deg,#eee,#fafafa)",
    disk: "linear-gradient(90deg,#ccc,#fff)"
  },
  red: {
    primary: "#d31027", light: "#ea384d",
    cpu: "linear-gradient(90deg,#8e0e00,#e52d27)",
    ram: "linear-gradient(90deg,#b31217,#e52d27)",
    disk: "linear-gradient(90deg,#cb2d3e,#ef473a)"
  },
  purple: {
    primary: "#9e53c0", light: "#d26fef",
    cpu: "linear-gradient(90deg,#42275a,#734b6d)",
    ram: "linear-gradient(90deg,#6441a5,#2a0845)",
    disk: "linear-gradient(90deg,#8e2de2,#4a00e0)"
  },
 yellow: {
        primary: "#FFD700", light: "#FFEC8B",
        cpu: "linear-gradient(90deg,#e6b800,#FFD700)",
        ram: "linear-gradient(90deg,#ffcc00,#ffee58)",
        disk: "linear-gradient(90deg,#f9d423,#ffdd00)"
      }
};

document.querySelectorAll(".theme-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const theme = themes[btn.dataset.theme];
    if (!theme) return;

    document.documentElement.style.setProperty("--primary", theme.primary);
    document.documentElement.style.setProperty("--primary-light", theme.light);
    document.documentElement.style.setProperty("--cpu-gradient", theme.cpu);
    document.documentElement.style.setProperty("--ram-gradient", theme.ram);
    document.documentElement.style.setProperty("--disk-gradient", theme.disk);
  });
});
});
  });