import requests
import datetime as dt
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy

API_KEY = 'da2c43a428accce3831de64096da4eeb'
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SECRET_KEY'] = 'super_secret_key'
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', cities=get_cities())


@app.route('/', methods=['POST'])
def add():
    city_name = request.form['city_name']
    add_city(city_name)
    return redirect(url_for('index'))


def to_celsius(degrees):
    degrees = int(degrees)
    celsius = (degrees - 32) * 5 / 9
    return "%.1f" % celsius


def add_city(city_name):
    weather = get_city_from_api(city_name)
    cod = weather['cod']
    if cod == '404' or city_name == '':
        flash('The city doesn\'t exist!')
        return

    city = City.query.filter_by(name=city_name).first()
    if city:
        flash('The city already stored in the database!')
        return

    city = City(name=city_name)
    db.session.add(city)
    db.session.commit()


def get_cities():
    cities = City.query.all()
    weather_data = []
    for city in cities:
        response = get_city_from_api(city.name)
        weather = {
            'city_name': city.name,
            'temp': to_celsius(response['main']['temp']),
            'main': response['weather'][0]['main'],
            'class_name': get_current_time_class(response['timezone'])
        }
        weather_data.append(weather)
    return weather_data


def get_city_from_api(city):
    global API_KEY
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={API_KEY}'
    response = requests.get(URL)
    weather = response.json()
    return weather


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
