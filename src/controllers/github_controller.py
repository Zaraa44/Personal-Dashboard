import os
import requests
from flask import Blueprint, jsonify
from dotenv import load_dotenv

load_dotenv()

github_bp = Blueprint("github", __name__)

GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def gh_get(url):
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    r = requests.get(url, headers=headers)

    # Debug logging
    print("GitHub API:", url, r.status_code)

    try:
        data = r.json()
    except Exception:
        return {"error": f"Invalid response from GitHub: {r.text}", "status": r.status_code}

    if r.status_code != 200:
        return {"error": data.get("message", "Unknown error"), "status": r.status_code}

    return data


@github_bp.route("/repos")
def repos():
    url = f"https://api.github.com/users/{GITHUB_USER}/repos"
    data = gh_get(url)

    if "error" in data:
        return jsonify(data), data.get("status", 500)

    repos = [{"name": r["name"], "url": r["html_url"]} for r in data]
    return jsonify(repos)


@github_bp.route("/<repo>/commits")
def commits(repo):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/commits"
    data = gh_get(url)

    if "error" in data:
        return jsonify(data), data.get("status", 500)

    commits = [
        {"msg": c["commit"]["message"], "author": c["commit"]["author"]["name"]}
        for c in data[:5]
    ]
    return jsonify(commits)


@github_bp.route("/<repo>/pulls")
def pulls(repo):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/pulls"
    data = gh_get(url)

    if "error" in data:
        return jsonify(data), data.get("status", 500)

    pulls = [{"title": p["title"], "url": p["html_url"]} for p in data]
    return jsonify(pulls)


@github_bp.route("/<repo>/issues")
def issues(repo):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/issues"
    data = gh_get(url)

    if "error" in data:
        return jsonify(data), data.get("status", 500)

    issues = [{"title": i["title"], "url": i["html_url"]} for i in data if "pull_request" not in i]
    return jsonify(issues)


@github_bp.route("/<repo>/info")
def info(repo):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}"
    data = gh_get(url)

    if "error" in data:
        return jsonify(data), data.get("status", 500)

    return jsonify({
        "name": data["name"],
        "description": data.get("description"),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0)
    })
