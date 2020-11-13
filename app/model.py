from app import db


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    apiadvisor_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'City {0}'.format(self.name)

    def jsonized(self):
        return {
            'name': f'{self.name}',
            'state': f'{self.state}',
            'country': f'{self.country}'
        }
    
    def get_or_create(self):
        city = City.query.one_or_none()

        if city is None:
            db.session.add(self)
            db.session.commit()
            return self.id

        return city.id

    
class Forecast(db.Model):
    __tablename__ = 'forecasts'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    date = db.Column(db.Date, index=True, nullable=False)
    probability = db.Column(db.Integer, nullable=False)
    precipitation = db.Column(db.Integer, nullable=False)
    minimum_temperature = db.Column(db.Integer, nullable=False)
    maximum_temperature = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Forecast in {0}'.format(self.date)

