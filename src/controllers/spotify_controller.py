from flask import Blueprint, redirect, request, session, render_template, jsonify
import requests, os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()
spotify_bp = Blueprint("spotify", __name__)


CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

SCOPE = "user-read-currently-playing user-read-playback-state user-modify-playback-state"


# === Routes ===

@spotify_bp.route("/login")
def login():
    auth_url = SPOTIFY_AUTH_URL + '?' + urlencode({
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    })
    return redirect(auth_url)


@spotify_bp.route("/callback")
def callback():
    code = request.args.get('code')
    response = requests.post(SPOTIFY_TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    response_data = response.json()

    session['spotify_token'] = response_data['access_token']
    session['spotify_refresh_token'] = response_data.get('refresh_token')  # opslaan!

    return redirect("/")



def refresh_spotify_token():
    refresh_token = session.get('spotify_refresh_token')
    if not refresh_token:
        return None

    response = requests.post(SPOTIFY_TOKEN_URL, data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    data = response.json()
    new_token = data.get('access_token')

    if new_token:
        session['spotify_token'] = new_token
    return new_token


def get_auth_headers():
    token = session.get('spotify_token')
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}


def get_current_playback(headers):
    res = requests.get(f"{SPOTIFY_API_BASE_URL}/me/player/currently-playing", headers=headers)
    if res.status_code == 204:
        return None
    if res.status_code != 200:
        raise Exception(f"Failed to fetch playback: {res.status_code}")
    return res.json()


def get_playlist_name(context, headers):
    if context and context.get("type") == "playlist":
        playlist_id = context["uri"].split(":")[-1]
        res = requests.get(f"{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}", headers=headers)
        if res.status_code == 200:
            return res.json().get("name")
    return None


def format_track_data(playback_data, playlist_name):
    item = playback_data.get("item")
    if not item:
        return {
            "name": None,
            "artists": None,
            "album_image": None,
            "progress_ms": 0,
            "duration_ms": 0,
            "popularity": 0,
            "album": None,
            "playlist": playlist_name,
            "is_playing": playback_data.get("is_playing", False)
        }

    return {
        "name": item["name"],
        "artists": ", ".join([artist["name"] for artist in item["artists"]]),
        "album_image": item["album"]["images"][0]["url"],
        "progress_ms": playback_data.get("progress_ms", 0),
        "duration_ms": item.get("duration_ms", 0),
        "popularity": item.get("popularity", 0),
        "album": item["album"]["name"],
        "playlist": playlist_name,
        "is_playing": playback_data.get("is_playing", False)
    }



# === API endpoints ===

@spotify_bp.route("/current")
def current_track():
    if "access_token" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    headers = get_auth_headers()

    try:
        playback_data = get_current_playback(headers)
        if not playback_data:
            return jsonify({"playing": False})

        playlist_name = get_playlist_name(playback_data.get("context"), headers)
        response = format_track_data(playback_data, playlist_name)
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@spotify_bp.route("/play", methods=["PUT"])
def play():
    headers = get_auth_headers()
    res = requests.put(f"{SPOTIFY_API_BASE_URL}/me/player/play", headers=headers)
    return jsonify(res.json() if res.content else {"status": res.status_code})


@spotify_bp.route("/pause", methods=["PUT"])
def pause():
    headers = get_auth_headers()
    res = requests.put(f"{SPOTIFY_API_BASE_URL}/me/player/pause", headers=headers)
    return jsonify(res.json() if res.content else {"status": res.status_code})


@spotify_bp.route("/next", methods=["POST"])
def next_track():
    headers = get_auth_headers()
    res = requests.post(f"{SPOTIFY_API_BASE_URL}/me/player/next", headers=headers)
    return jsonify(res.json() if res.content else {"status": res.status_code})


@spotify_bp.route("/previous", methods=["POST"])
def prev_track():
    headers = get_auth_headers()
    res = requests.post(f"{SPOTIFY_API_BASE_URL}/me/player/previous", headers=headers)
    return jsonify(res.json() if res.content else {"status": res.status_code})
