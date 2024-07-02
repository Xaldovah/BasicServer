from flask import Flask, request, jsonify
import requests
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

WEATHER_API_KEY = '814ff9aed0f8900a97ae0832af2cd3a4'
GEOLOCATION_API_KEY = 'f188689a3c6b4a8c976fa00150cf7ce4'

@app.route('/api/hello')
def hello():
    visitor_name = request.args.get('visitor_name', 'visitor')
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print(client_ip)

    geo_response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={GEOLOCATION_API_KEY}')
    geo_data = geo_response.json()
    city = geo_data.get('city', 'Unknown')
    print(city)

    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric')
    weather_data = weather_response.json()

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
