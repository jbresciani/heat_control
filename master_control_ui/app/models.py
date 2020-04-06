import logging
from .extensions import db, ma

logger = logging.getLogger(__name__)


class Thermostats(db.Model):
    __tablename__ = 'thermostats'
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True)
    group = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256))
    url = db.Column(db.String(128))
    current_temp = db.Column(db.Integer, default=15)
    requested_temp = db.Column(db.Integer, default=15)

    @classmethod
    def update_row(cls, data):
        ''' update a row in sqlite

        Inputs:
            cls  (obj) - the class object, this is not directly passed in
            data (dict) - the information to be updated, must contain at least thermostat id and one other key
        '''
        cls.query.filter(cls.id == data['id']).update(data)
        db.session.commit()

    @classmethod
    def get_thermostats(cls):
        thermostat_data = cls.query.all()
        thermostat_schema = ThermostatsSchema(many=True)
        return thermostat_schema.dump(thermostat_data)


class ThermostatsSchema(ma.ModelSchema):
    class Meta:
        model = Thermostats
        sqla_session = db.session
