import os
from flask.globals import session
import requests
from app import app, db
from datetime import datetime
from flask import request
from app.model import City, Forecast
from sqlalchemy.sql import func


@app.route('/city', methods=['GET', 'POST'])
def city():
    param_city_id = request.args.get('id', None)
    if (param_city_id == None):
        return { 'reason': 'Missing id param' }, 400

    if request.method == 'GET':
        city = db.session.query(City).filter_by(apiadvisor_id=param_city_id).scalar()
        if city is not None:
            return city.jsonized(), 200
        return 'Not found', 404

    param_days = request.args.get('days', None)
    if (param_days == None):
        return { 'reason': 'Missing id param' }, 400

    token = os.getenv('WEATHER_API_TOKEN')
    url = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{0}' \
          '/days/{1}?token={2}'.format(param_city_id, param_days, token)

    forecast = requests.get(url).json()

    if (forecast.get('error') == True):
        return 'Not found', 404

    city_detail = City(
        name=forecast.get('name'),
        state=forecast.get('state'),
        country=forecast.get('country'),
        apiadvisor_id=int(param_city_id)
    )
    city_id = city_detail.get_or_create()

    forecasts = []
    forecasts_to_show_in_return = []

    for i in forecast.get('data'):
        forecasts_to_show_in_return.append({
            'date': i.get('date'),
            'probability': i.get('rain').get('probability'),
            'precipitation': i.get('rain').get('precipitation'),
            'minimum_temperature': i.get('temperature').get('min'),
            'maximum_temperature': i.get('temperature').get('max')
        })
        forecasts.append(Forecast(
            city_id=city_id,
            date=datetime.strptime(i.get('date'), "%Y-%m-%d"),
            probability=i.get('rain').get('probability'),
            precipitation=i.get('rain').get('precipitation'),
            minimum_temperature=i.get('temperature').get('min'),
            maximum_temperature=i.get('temperature').get('max'),
        ))

    db.session.bulk_save_objects(forecasts)
    db.session.commit()

    return {
        'city_detail': city_detail.jsonized(),
        'data': forecasts_to_show_in_return
    }, 201   


@app.route('/analyze', methods=['GET'])
def analyze():
    initial_date = request.args.get('initial_date', None)
    if (initial_date == None):
        return { 'reason': 'Missing initial_date param' }, 400

    final_date = request.args.get('final_date', None)
    if (final_date == None):
        return { 'reason': 'Missing final_date param' }, 400

    if (initial_date >= final_date):
        return { 'reason': 'The initial_date must be less than the final_date' }

    city_with_maximum_temperature = db.session.query(
            Forecast.maximum_temperature.label('temperature'),
            City.name.label('name'),
            Forecast.date   
        ).join(
            Forecast,
            City.id == Forecast.city_id
        ).filter(
            Forecast.date.between(initial_date, final_date)
        ).order_by(Forecast.maximum_temperature.desc()).first()

    if city_with_maximum_temperature is None:
        return 'No data registered on that date', 404

    forecasts_avg = db.session.query(
        City.name.label('city_name'),
        func.avg(Forecast.precipitation).label('avg_precipitation')
    ).join(
        Forecast,
        City.id == Forecast.city_id
    ).filter(
        Forecast.date.between(initial_date, final_date)).group_by(Forecast.city_id)

    forecasts_avg_to_show_in_return = []
    for forecast_avg in forecasts_avg:
        forecasts_avg_to_show_in_return.append({
            'city_name': forecast_avg.city_name,
            'avg_precipitation': forecast_avg.avg_precipitation
        })

    return {
        'city_with_maximum_temperature': {
            'city_name': city_with_maximum_temperature.name,
            'temperature': city_with_maximum_temperature.temperature,
            'date': city_with_maximum_temperature.date
        },
        'cities_precipitation': forecasts_avg_to_show_in_return,
    }, 200