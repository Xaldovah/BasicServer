from flask import Flask, request, jsonify
import requests
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

WEATHER_API_KEY = '814ff9aed0f8900a97ae0832af2cd3a4'
GEOLOCATION_API_KEY = 'f188689a3c6b4a8c976fa00150cf7ce4'

def get_client_ip():
    # The client IP is the first IP in the list from X-Forwarded-For
    if 'X-Forwarded-For' in request.headers:
        client_ip = request.headers['X-Forwarded-For'].split(',')[0]
        print(f"Client IP from X-Forwarded-For header: {client_ip}")
        return client_ip

    # Fallback to remote address
    client_ip = request.remote_addr
    print(f"Client IP from request.remote_addr: {client_ip}")
    return client_ip


@app.route('/api/hello')
def hello():
    visitor_name = request.args.get('visitor_name', 'visitor')
    client_ip = get_client_ip()

    # Use the ipgeolocation.io API to get location data
    geo_response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={GEOLOCATION_API_KEY}')
    geo_data = geo_response.json()
    city = geo_data.get('city', 'Unknown')

    # Log the response for debugging purposes
    print("Geolocation API Response:", geo_data)

    # Use the OpenWeatherMap API to get weather data
    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric')
    weather_data = weather_response.json()

    # Log the response for debugging purposes
    print("Weather API Response:", weather_data)

    if weather_data.get('main'):
        temperature = weather_data['main']['temp']
        greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    else:
        greeting = f"Hello, {visitor_name}!, we could not retrieve the temperature for {city}"

    return jsonify({
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    })


if __name__ == '__main__':
    app.run(debug=True)
