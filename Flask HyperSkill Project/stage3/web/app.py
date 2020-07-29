import requests
from flask import Flask
from flask import render_template
from flask import request
import datetime as dt

API_KEY = 'da2c43a428accce3831de64096da4eeb'
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def add():
    city_name = request.form['city_name']
    temp, main, class_name_for_current_time = get_city_weather(city_name)
    return render_template('index.html', temp=temp, main=main, city_name=city_name,
                           class_name=class_name_for_current_time)


def to_celsius(degrees):
    degrees = int(degrees)
    celsius = (degrees - 32) * 5 / 9
    return "%.1f" % celsius


def get_city_weather(city_name):
    global API_KEY
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={API_KEY}'
    response = requests.get(URL)
    weather = response.json()
    main = weather['weather'][0]['main']
    temp = to_celsius(weather['main']['temp'])
    class_name_for_current_time = get_current_time_class(weather['timezone'])
    print(class_name_for_current_time)
    return temp, main, class_name_for_current_time


def get_current_time_class(timezone):
    temp = dt.datetime.utcnow() + dt.timedelta(0, timezone)
    time = temp.time()
    print(time)
    if dt.time(0, 0, 0) < time <= dt.time(6, 0, 0):
        return 'night'
    if dt.time(6, 0, 0) < time <= dt.time(12, 0, 0):
        return 'evening-morning'
    if dt.time(12, 0, 0) < time <= dt.time(18, 0, 0):
        return 'day'
    if dt.time(18, 0, 0) < time <= dt.time(23, 59, 59):
        return 'night'


if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.107')
