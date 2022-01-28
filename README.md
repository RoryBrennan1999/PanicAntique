# Flask-RESTful App written in Python

## Supporting Libraries: flask, flask-restful, random

### Operation is as follows:
- Allows registering of sensors to REST API (has initially two sensors)
- Sensor data display host country, city and previous temperature, humidity and wind speed data for previous 30 days (stored in JSON)
- Supports patching and deleting of existing data
- New sensors can be posted from existing JSON files
- Averages of weather data can be displayed in day ranges (E.g Day 1 to Day 7)
- Input validation when posting and patching
- Error handling (E.g sensor ID doesnt exist)

### Included are four test files to test operations:
- bad_sensor.json
- new_sensor.json
- patch_test_1.json
- patch_test_2.json

### Test commands include (I suggest using these curl commands from a Linux terminal such as WSL):
- curl -i http://127.0.0.1:5000/sensors
- curl -i http://127.0.0.1:5000/sensors -X POST -H 'Content-Type: application/json' --data @new_sensor.json
- curl -i http://127.0.0.1:5000/sensors -X POST -H 'Content-Type: application/json' --data @bad_sensor.json
- curl -i http://127.0.0.1:5000/sensors/sensor2
- curl http://127.0.0.1:5000/sensors/sensor1 -d "city=Dublin"  -X PATCH -v
- curl http://127.0.0.1:5000/sensors/sensor1 -d "country=Ireland"  -X PATCH -v
- curl http://127.0.0.1:5000/sensors/sensor1 -d @patch_test_1.json -X PATCH -H "Content-Type: application/json"
- curl http://127.0.0.1:5000/sensors/sensor1 -d @patch_test_2.json -X PATCH -H "Content-Type: application/json"
- curl -i http://127.0.0.1:5000/sensors/sensor1 -X DELETE -v
- curl -i http://127.0.0.1:5000/sensors/sensor2/ave/7
- curl -i http://127.0.0.1:5000/sensors/sensor2/ave/30
- curl -i http://127.0.0.1:5000/sensors/sensor2/ave/1

### Run Command: python app.py
