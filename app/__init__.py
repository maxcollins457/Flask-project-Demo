from flask import Flask

from app.views.home import home_bp
from app.views.weather import weather_bp
from app.views.extras import extras_bp

# Set up the flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.register_blueprint(home_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(extras_bp)

