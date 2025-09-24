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
    return r.json()

@github_bp.route("/repos")
def repos():
    url = f"https://api.github.com/users/{GITHUB_USER}/repos"
    data = gh_get(url)
    repos = [{"name": r["name"], "url": r["html_url"]} for r in data]
    return jsonify(repos)

@github_bp.route("/<repo>/commits")
def commits(repo):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/commits"
    data = gh_get(url)
    commits = [{"msg": c["commit"]["message"], "author": c["commit"]["author"]["name"]} for c in data[:5]]
    return jsonify(commits)

@github_bp.route("/<repo>/pulls")
def pulls(repo):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/pulls"
    data = gh_get(url)
    pulls = [{"title": p["title"], "url": p["html_url"]} for p in data]
    return jsonify(pulls)

@github_bp.route("/<repo>/issues")
def issues(repo):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/issues"
    data = gh_get(url)
    issues = [{"title": i["title"], "url": i["html_url"]} for i in data if "pull_request" not in i]
    return jsonify(issues)

@github_bp.route("/<repo>/info")
def info(repo):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}"
    r = gh_get(url)
    return jsonify({
        "name": r["name"],
        "description": r["description"],
        "stars": r["stargazers_count"],
        "forks": r["forks_count"]
    })
