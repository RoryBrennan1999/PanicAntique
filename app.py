
###########################
# Flask RESTful Web App   #
# Rory Brennan            #
# 28/01/2022              #
###########################

# Import modules
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import random

# Create Flask App and API
app = Flask(__name__)
api = Api(app)

# Initial sensors posted on API (random range to give list of temps, humidity etc)
# Temp data is list of 30 integers representing previous 30 days i.e. temp index 0 is most recent temp reading
sensors = {
    'sensor1': {"country": "Thailand", "city": "Bangkok", "temp": [random.randrange(15, 50, 1) for i in range(30)],
                "humidity": [random.randrange(75, 100, 1) for i in range(30)],
                "wind speed": [random.randrange(1, 15, 1) for i in range(30)]},
    'sensor2': {"country": "Ireland", "city": "Dublin", "temp": [random.randrange(1, 20, 1) for i in range(30)],
                "humidity": [random.randrange(40, 90, 1) for i in range(30)],
                "wind speed": [random.randrange(1, 25, 1) for i in range(30)]},
}

# Helper Functions
def abort_if_sensor_doesnt_exist(sensor_id):
    if sensor_id not in sensors:
        abort(404, message="Sensor {} doesn't exist".format(sensor_id))

def calculate_average(input_list, range):

    # If range is only 1 day, return most recent data
    if range == "1":
        return input_list[0]

    sum = 0
    index = 0
    while index != (int(range)-1):
        sum = sum + input_list[index]
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


# Parser for parsing curl arguments (also define types of input)
parser = reqparse.RequestParser()
parser.add_argument("country", type=str)
parser.add_argument("city", type=str)
parser.add_argument("temp", type=int, action='append')
parser.add_argument("humidity", type=int, action='append')
parser.add_argument("wind speed", type=int, action='append')

# Averages class
# range: Date range of average Eg. 7 for most recent week
# sensor_id: ID of sensor for average
class Averages(Resource):
    def get(self, sensor_id, range):
        if int(range) > 30:
            abort(404, message="Cannot calculate averages beyond previous 30 days")

        abort_if_sensor_doesnt_exist(sensor_id)
        return {"ID": sensor_id, "range": f"Day 1 to Day {range}", "average temp": calculate_average(sensors[sensor_id]["temp"], range), "average wind speed": calculate_average(sensors[sensor_id]["wind speed"], range), "average humidity": calculate_average(sensors[sensor_id]["humidity"], range)}


# Singular sensor class
# Can be patched (updated), deleted and its data displayed
class Sensor(Resource):
    def get(self, sensor_id):
        abort_if_sensor_doesnt_exist(sensor_id)
        return sensors[sensor_id]

    def delete(self, sensor_id):
        abort_if_sensor_doesnt_exist(sensor_id)
        del sensors[sensor_id]
        return '', 204

    # Supports both typed curl arguments aswell as JSON input files
    def patch(self, sensor_id):
        args = parser.parse_args()
        if args["country"] is not None:
            if is_data_valid(args["country"], str):
                sensors[sensor_id]["country"] = args["country"]
            else:
                abort(404, message="Input country metadata is invalid, please fix!")
        if args["city"] is not None:
            if is_data_valid(args["city"], str):
                sensors[sensor_id]["city"] = args["city"]
            else:
                abort(404, message="Input city metadata is invalid, please fix!")
        if args["temp"] is not None:
            if is_data_valid(args["temp"], int):
                for index, item in enumerate(args["temp"]):
                    sensors[sensor_id]["temp"][index] = args["temp"][index]
            else:
                abort(404, message="Input temp data is invalid, please fix!")
        if args["humidity"] is not None:
            if is_data_valid(args["humidity"], int):
                for index, item in enumerate(args["humidity"]):
                    sensors[sensor_id]["humidity"][index] = args["humidity"][index]
            else:
                abort(404, message="Input humidity data is invalid, please fix!")
        if args["wind speed"] is not None:
            if is_data_valid(args["wind speed"], int):
                for index, item in enumerate(args["wind speed"]):
                    sensors[sensor_id]["wind speed"][index] = args["wind speed"][index]
            else:
                abort(404, message="Input wind speed data is invalid, please fix!")
        return sensors[sensor_id], 201


# Entire sensors list class
class SensorsList(Resource):
    def get(self):
        return sensors

    # Supports both typed curl arguments aswell as JSON input files
    def post(self):
        if request.is_json:
            sensor = request.get_json()
            if not is_data_valid(sensor["country"], str):
                abort(404, message="Input country metadata is invalid, please fix!")
            if not is_data_valid(sensor["city"], str):
                abort(404, message="Input city metadata is invalid, please fix!")
            if not is_data_valid(sensor["temp"], int):
                abort(404, message="Input temp data is invalid, please fix!")
            if not is_data_valid(sensor["humidity"], int):
                abort(404, message="Input humidity data is invalid, please fix!")
            if not is_data_valid(sensor["wind speed"], int):
                abort(404, message="Input wind speed data is invalid, please fix!")
            id_num = int(max(sensors.keys()).lstrip('sensor')) + 1
            sensor_id = "sensor%i" % id_num
            sensors[sensor_id] = sensor
            return sensors[sensor_id], 201
        else:
            args = parser.parse_args()
            if not is_data_valid(args["country"], str):
                abort(404, message="Input country metadata is invalid, please fix!")
            if not is_data_valid(args["city"], str):
                abort(404, message="Input city metadata is invalid, please fix!")
            if not is_data_valid(args["temp"], int):
                abort(404, message="Input temp data is invalid, please fix!")
            if not is_data_valid(args["humidity"], int):
                abort(404, message="Input humidity data is invalid, please fix!")
            if not is_data_valid(args["wind speed"], int):
                abort(404, message="Input wind speed data is invalid, please fix!")
            id_num = int(max(sensors.keys()).lstrip('sensor')) + 1
            sensor_id = "sensor%i" % id_num
            sensors[sensor_id] = {"country": args["country"], "city": args["city"], "temp": args["temp"], "humidity": args["humidity"], "wind speed": args["wind speed"]}
            return sensors[sensor_id], 201


# Add previous resources to API
api.add_resource(SensorsList, '/sensors')
api.add_resource(Sensor, '/sensors/<sensor_id>')
api.add_resource(Averages, '/sensors/<sensor_id>/ave/<range>')

# Run App
if __name__ == '__main__':
    app.run(debug=True)
