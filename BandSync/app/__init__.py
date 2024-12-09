from flask import Flask

app = Flask(__name__)

from app import band_matcher, scheduler, ai_composer, music_analyzer, user_profiles 