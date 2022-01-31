# Flask-RESTful App written in Python

## Supporting Libraries: see requirements.txt

### Operation is as follows:
- Allows registering of sensors to REST API (has initially two sensors)
- Sensor data display host country, city and previous temperature, humidity and wind speed data for previous 30 days (stored in JSON)
- Supports patching and deleting of existing data
- New sensors can be posted from existing JSON files
- Averages of weather data can be displayed in day ranges (E.g Day 1 to Day 7)
- Input validation when posting and patching
- Error handling (E.g sensor ID doesnt exist)

### Run Command: python app.py

### Run test suite: python app_test.py
