function shortenCommitMessage(msg, maxWords = 5) {
  const words = msg.split(" ");
  if (words.length > maxWords) {
    return words.slice(0, maxWords).join(" ") + " ...";
  }
  return msg;
}

async function loadRepos() {
  const res = await fetch("/api/github/repos");
  const repos = await res.json();
  const select = document.getElementById("repo-select");

  select.innerHTML = repos.map(r => `<option value="${r.name}">${r.name}</option>`).join("");

  select.addEventListener("change", () => loadRepoData(select.value));

  if (repos.length > 0) {
    loadRepoData(repos[0].name);
  }
}

async function loadRepoData(repo) {
  const info = await (await fetch(`/api/github/${repo}/info`)).json();
  const commits = await (await fetch(`/api/github/${repo}/commits`)).json();
  const pulls = await (await fetch(`/api/github/${repo}/pulls`)).json();
  const issues = await (await fetch(`/api/github/${repo}/issues`)).json();

  document.getElementById("repo-info").innerHTML =
    `<p><b>${info.name}</b><br>${info.description || "No description"}</p>`;

  document.getElementById("repo-commits").innerHTML =
    commits.map(c => `
      <div class="commit-item">
        <div class="commit-message">${shortenCommitMessage(c.msg)}</div>
        <div class="commit-author">— ${c.author}</div>
      </div>
    `).join("");

  document.getElementById("repo-pulls").innerHTML =
    pulls.map(p => `<a href="${p.url}" target="_blank">${p.title}</a>`).join("");

  document.getElementById("repo-issues").innerHTML =
    issues.map(i => `<a href="${i.url}" target="_blank">${i.title}</a>`).join("");
}

loadRepos();
