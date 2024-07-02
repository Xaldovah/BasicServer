from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


GEOLOCATION_API_KEY = '1748adbe49b6bd2a45bbd274e237f99a'
WEATHER_API_KEY = '814ff9aed0f8900a97ae0832af2cd3a4'


@app.route('/api/hello')
def hello():
    visitor_name = request.args.get('visitor_name', 'visitor')
    client_ip = request.remote_addr

    geo_response = requests.get(f'http://api.ipstack.com/{client_ip}?access_key={GEOLOCATION_API_KEY}')
    geo_data = geo_response.json()
    print(geo_data)
    city = geo_data.get('city')
    print(city)

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
