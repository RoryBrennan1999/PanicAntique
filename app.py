
###########################
# Flask RESTful Web App   #
# Rory Brennan            #
# 31/01/2022              #
###########################

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppress warning
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))
    temp = db.Column(db.String(50), default='0.0')
    humidity = db.Column(db.String(50), default='0.0')
    wind_speed = db.Column(db.String(50), default='0.0')

    def __repr__(self):
        return '<Sensor %s>' % self.id


class SensorSchema(ma.Schema):
    class Meta:
        fields = ("id", "country", "city", "temp", "humidity", "wind_speed")

sensor_schema = SensorSchema()
sensors_schema = SensorSchema(many=True)

# Helper Functions
def calculate_average(input_list, range):

    # Convert string to list of integers
    ints = [int(x) for x in input_list.split(', ')]

    # If range is only 1 day, return most recent data
    if range == "1":
        return input_list[0]

    sum = 0
    index = 0
    while index != (int(range)-1):
        sum = sum + ints[index]
        index = index + 1

    return sum/int(range)

def is_data_valid(input_data, expected_type):
    if expected_type is int:
        return all(isinstance(elem, int) for elem in input_data)
    elif expected_type is str:
        if type(input_data) is str:
            return True
        else:
            return False

# Averages class
# range: Date range of average Eg. 7 for most recent week
# sensor_id: ID of sensor for average
class Averages(Resource):
    def get(self, sensor_id, range):
        if int(range) > 30:
            abort(404, message="Cannot calculate averages beyond previous 30 days")

        sensor = Sensor.query.get_or_404(sensor_id)
        return {"ID": sensor_id, "range": f"Day 1 to Day {range}", "average temp": calculate_average(sensor.temp, range), "average humidity": calculate_average(sensor.humidity, range), "average wind speed": calculate_average(sensor.wind_speed, range)}

class SensorsList(Resource):
    def get(self):
        sensors = Sensor.query.all()
        return sensors_schema.dump(sensors)

    def post(self):
        new_sensor = Sensor(country=request.json['country'], city=request.json['city'], temp=request.json['temp'], humidity=request.json['humidity'], wind_speed=request.json['wind speed'])
        if not is_data_valid(new_sensor.country, str):
            abort(404, message="Input country metadata is invalid, please fix!")
        if not is_data_valid(new_sensor.city, str):
            abort(404, message="Input city metadata is invalid, please fix!")
        if not is_data_valid(new_sensor.temp, str):
            abort(404, message="Input temp data is invalid, please fix!")
        if not is_data_valid(new_sensor.humidity, str):
            abort(404, message="Input humidity data is invalid, please fix!")
        if not is_data_valid(new_sensor.wind_speed, str):
            abort(404, message="Input wind speed data is invalid, please fix!")
        db.session.add(new_sensor)
        db.session.commit()
        return sensor_schema.dump(new_sensor)


class SensorResource(Resource):
    def get(self, sensor_id):
        sensor = Sensor.query.get_or_404(sensor_id)
        return sensor_schema.dump(sensor)

    def patch(self, sensor_id):
        sensor = Sensor.query.get_or_404(sensor_id)

        if 'country' in request.json:
            if is_data_valid(request.json['country'], str):
                sensor.country = request.json['country']
            else:
                abort(404, message="Input country metadata is invalid, please fix!")
        if 'city' in request.json:
            if is_data_valid(request.json['city'], str):
                sensor.city = request.json['city']
            else:
                abort(404, message="Input city metadata is invalid, please fix!")
        if 'temp' in request.json:
            if is_data_valid(request.json['temp'], str):
                sensor.temp = request.json['temp']
            else:
                abort(404, message="Input temp data is invalid, please fix!")
        if 'humidity' in request.json:
            if is_data_valid(request.json['humidity'], str):
                sensor.humidity = request.json['humidity']
            else:
                abort(404, message="Input humidity data is invalid, please fix!")
        if 'wind speed' in request.json:
            if is_data_valid(request.json['wind speed'], str):
                sensor.wind_speed = request.json['wind speed']
            else:
                abort(404, message="Input wind speed data is invalid, please fix!")

        db.session.commit()
        return sensor_schema.dump(sensor)

    def delete(self, sensor_id):
        sensor = Sensor.query.get_or_404(sensor_id)
        db.session.delete(sensor)
        db.session.commit()
        return '', 204


api.add_resource(SensorsList, '/sensors')
api.add_resource(SensorResource, '/sensors/<int:sensor_id>')
api.add_resource(Averages, '/sensors/<sensor_id>/ave/<range>')

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

