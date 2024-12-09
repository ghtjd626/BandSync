from flask import Flask, render_template, request, redirect, url_for
from app.band_matcher import BandMatcher

app = Flask(__name__)

# Initialize the BandMatcher
matcher = BandMatcher()

@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    """Add a new user."""
    if request.method == "POST":
        name = request.form["name"]
        sessions = request.form["sessions"]
        skill = request.form["skill"]
        location = request.form["location"]
        genres = request.form["genres"]
        matcher.add_user(name, sessions, skill, location, genres)
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/add_band", methods=["GET", "POST"])
def add_band():
    """Add a new band."""
    if request.method == "POST":
        name = request.form["name"]
        recruiting_sessions = request.form["recruiting_sessions"]
        required_skill = request.form["required_skill"]
        location = request.form["location"]
        genres = request.form["genres"]
        matcher.add_band(name, recruiting_sessions, required_skill, location, genres)
        return redirect(url_for("index"))
    return render_template("add_band.html")

@app.route("/matches")
def matches():
    """Show matches."""
    results = matcher.match()
    return render_template("matches.html", matches=results)

if __name__ == "__main__":
    app.run(debug=True)
