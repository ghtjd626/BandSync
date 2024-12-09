from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Import routes
    from .routes import band_routes
    app.register_blueprint(band_routes)

    return app
