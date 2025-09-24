from flask import Blueprint, redirect, request, session, jsonify
import requests, os
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()
google_bp = Blueprint("google", __name__)

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
CAL_API = "https://www.googleapis.com/calendar/v3"

SCOPE = "https://www.googleapis.com/auth/calendar.readonly"

@google_bp.route("/login")
def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }
    return redirect(AUTH_URL + "?" + urlencode(params))

@google_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No code"}), 400

    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    res = requests.post(TOKEN_URL, data=token_data)
    tokens = res.json()

    session["google_token"] = tokens.get("access_token")
    return redirect("/")

@google_bp.route("/events")
def events():
    if "google_token" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    headers = {"Authorization": f"Bearer {session['google_token']}"}
    res = requests.get(f"{CAL_API}/calendars/primary/events?maxResults=5&orderBy=startTime&singleEvents=true", headers=headers)

    return jsonify(res.json())
