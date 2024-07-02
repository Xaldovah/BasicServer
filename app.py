from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WEATHER_API_KEY = '814ff9aed0f8900a97ae0832af2cd3a4'
GEOLOCATION_API_KEY = 'f188689a3c6b4a8c976fa00150cf7ce4'

def get_client_ip():
    if 'X-Forwarded-For' in request.headers:
        return request.headers['X-Forwarded-For'].split(',')[0]
    return request.remote_addr


@app.route('/api/hello')
def hello():
    visitor_name = request.args.get('visitor_name', 'visitor')
    client_ip = get_client_ip()

    # Use the ipgeolocation.io API to get location data
    geo_response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={GEOLOCATION_API_KEY}')
    geo_data = geo_response.json()
    city = geo_data.get('city', 'Unknown')

    # Use the OpenWeatherMap API to get weather data
    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric')
    weather_data = weather_response.json()
    temperature = weather_data['main']['temp']
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

    return jsonify({
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    })


if __name__ == '__main__':
    app.run(debug=True)
