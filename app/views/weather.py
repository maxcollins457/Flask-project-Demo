from flask import Blueprint, render_template, request, session

from app.models import get_current_weather, times_and_temps, temp_graph, get_city_pictures

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather-form', methods=['GET', 'POST'])
def weather():
    user_input = {}

    if request.method == 'POST':
        user_input['location'] = request.form['location']
        session['location'] = user_input['location']

        # Form validation
        if not user_input['location']:
            return render_template('weather-form.html', error_message="Please fill in location.")
    return render_template('weather-form.html')

@weather_bp.route('/weather-report')
def weather_report():
    location = session['location']
    weather_data, condition, icon_url = get_current_weather(location)

    #Generate the temperature graph
    temp_graph(location)

    #get some a picture of the city
    city_image_url = get_city_pictures(location)

    return render_template('weather-report.html', 
                           weather_data=weather_data,
                           condition= condition,
                           icon_url=icon_url,
                           city_image_url = city_image_url,
                           times_and_temps=times_and_temps, 
                           location=location)