from flask import Flask, render_template, request, redirect, url_for, jsonify
from app.band_matcher import BandMatcher

app = Flask(__name__)
matcher = BandMatcher()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        try:
            name = request.form['name']
            sessions = [s.strip() for s in request.form['sessions'].split(',')]
            skills = request.form['skills']
            location = request.form['location']
            
            # 장르와 선호도 데이터 처리 개선
            genres = [1 if x.strip().lower() == 'true' else 0 
                     for x in request.form['genres'].split(',')]
            preferences = [1 if x.strip().lower() == 'true' else 0 
                         for x in request.form['preferences'].split(',')]
            
            matcher.add_user(name, sessions, skills, location, genres, preferences)
            return redirect(url_for('home'))
        except Exception as e:
            return f"Error: {str(e)}", 400
            
    return render_template('add_user.html')

@app.route('/add_band', methods=['GET', 'POST'])
def add_band():
    if request.method == 'POST':
        try:
            name = request.form['name']
            recruiting_sessions = [s.strip() for s in request.form['recruiting_sessions'].split(',')]
            required_skills = request.form['required_skills']
            location = request.form['location']
            
            # 장르와 선호도 데이터 처리 개선
            genres = [1 if x.strip().lower() == 'true' else 0 
                     for x in request.form['genres'].split(',')]
            preferences = [1 if x.strip().lower() == 'true' else 0 
                         for x in request.form['preferences'].split(',')]
            
            matcher.add_band(name, recruiting_sessions, required_skills, location, genres, preferences)
            return redirect(url_for('home'))
        except Exception as e:
            return f"Error: {str(e)}", 400
            
    return render_template('add_band.html')

@app.route('/match')
def match():
    matches = matcher.match()
    return render_template('match.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True)
