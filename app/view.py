import requests
from app import app
from flask import request


@app.route('/city')
def city():
    city_id = request.args.get('id', None)

    if (city_id == None):
        return { 'reason': 'Missing city_id param' }, 400

    token = ''
    url = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{0}' \
          '/days/15?token={1}'.format(city_id, token)

    forecast = requests.get(url).json()

    if (forecast.get('error') == True):
        return { 'reason': forecast.get('detail') }, 400

    forecasts = []
    city_detail = {
        'name': forecast.get('name'),
        'state': forecast.get('state'),
        'country': forecast.get('country'),
    }

    for i in forecast.get('data'):
        forecasts.append({
            'date': i.get('date'),
            'brazilian_date': i.get('date_br'),
            'probability': i.get('rain').get('probability'),
            'precipitation': i.get('rain').get('precipitation'),
            'minimum_temperature': i.get('temperature').get('min'),
            'maximum_temperature': i.get('temperature').get('max')
        })

    return {
        'city_detail': city_detail,
        'data': forecasts
    }, 201   
