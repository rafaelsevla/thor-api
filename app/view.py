import os
import requests
from app import app, db
from datetime import datetime
from flask import request
from app.model import City, Forecast


@app.route('/city', methods=['GET', 'POST'])
def city():
    param_city_id = request.args.get('id', None)
    if (param_city_id == None):
        return { 'reason': 'Missing id param' }, 400

    if request.method == 'GET':
        city = db.session.query(City).filter(City.apiadvisor_id == param_city_id).scalar()
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
        return { 'reason': forecast.get('detail') }, 400

    city_detail = City(
        name=forecast.get('name'),
        state=forecast.get('state'),
        country=forecast.get('country'),
        apiadvisor_id=param_city_id
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