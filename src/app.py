from flask import Flask, render_template
from .controllers.spotify_controller import spotify_bp
from .controllers.github_controller import github_bp
import os
from dotenv import load_dotenv
from .controllers.system_controller import system_bp
from src.controllers.google_controller import google_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devsecret")

# Register blueprints
app.register_blueprint(spotify_bp, url_prefix="/api/spotify")
app.register_blueprint(github_bp, url_prefix="/api/github")
app.register_blueprint(google_bp, url_prefix="/api/google")

app.register_blueprint(system_bp, url_prefix="/api/system")


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
