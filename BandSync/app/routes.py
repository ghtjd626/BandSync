from flask import Blueprint, render_template, request, redirect, url_for, flash
from .band_matcher import BandMatcher

band_routes = Blueprint('band_routes', __name__)
matcher = BandMatcher()

@band_routes.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@band_routes.route('/add', methods=['GET', 'POST'])
def add_user_band():
    """Add users or bands."""
    if request.method == 'POST':
        entity_type = request.form['entity_type']
        name = request.form['name']
        location = request.form['location']
        if entity_type == 'user':
            sessions = request.form['sessions']
            skill = request.form['skill']
            genres = request.form['genres']
            matcher.add_user(name, sessions, skill, location, genres)
        elif entity_type == 'band':
            recruiting_sessions = request.form['recruiting_sessions']
            required_skill = request.form['required_skill']
            genres = request.form['genres']
            matcher.add_band(name, recruiting_sessions, required_skill, location, genres)
        flash(f"{entity_type.capitalize()} '{name}' added successfully!", "success")
        return redirect(url_for('band_routes.index'))
    return render_template('add_user_band.html')

@band_routes.route('/match', methods=['GET'])
def match():
    """Show matching results."""
    matches = matcher.match()
    return render_template('match.html', matches=matches)
