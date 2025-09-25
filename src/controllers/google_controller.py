from flask import Blueprint, redirect, request, session, jsonify
import requests, os
from urllib.parse import urlencode
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

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
    session["google_refresh_token"] = tokens.get("refresh_token")  # opslaan!

    return redirect("/")

def refresh_google_token():
    refresh_token = session.get("google_refresh_token")
    if not refresh_token:
        return None

    res = requests.post(TOKEN_URL, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    })
    data = res.json()
    new_token = data.get("access_token")

    if new_token:
        session["google_token"] = new_token
    return new_token

@google_bp.route("/events")
def events():
    if "google_token" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    headers = {"Authorization": f"Bearer {session['google_token']}"}

    now = datetime.now(timezone.utc).isoformat()

    params = {
        "maxResults": 8,
        "orderBy": "startTime",
        "singleEvents": True,
        "timeMin": now
    }

    res = requests.get(f"{CAL_API}/calendars/primary/events", headers=headers, params=params)

    if res.status_code == 401:  # token expired
        print("Google token expired, refreshing...")
        new_token = refresh_google_token()
        if not new_token:
            return jsonify({"error": "Unable to refresh token"}), 401
        headers = {"Authorization": f"Bearer {session['google_token']}"}
        res = requests.get(f"{CAL_API}/calendars/primary/events", headers=headers, params=params)

    return jsonify(res.json())
