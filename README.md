# AirQualityChecker-basic

A Django web app that lets users check the current air quality index (AQI) for any location by entering a city, state/province/region, and country (or just city and state for US locations). The app uses the Open-Meteo Air Quality API and Nominatim geocoding to fetch and display AQI, main pollutant, measurement time, and a health advisory. It includes both client-side and server-side validation, and handles errors gracefully.

## Features
- Simple form for entering location details
- Required fields: City and State/Province/Region
- Optional field: Country (defaults to USA)
- Client-side and server-side validation
- Converts location to coordinates using Nominatim (OpenStreetMap)
- Fetches AQI and air quality data from Open-Meteo (no API key required)
- Displays AQI, main pollutant, measurement time, and health advisory
- User-friendly error messages for invalid locations or API issues
- Unit and integration tests for form, API logic, and view rendering

## Getting Started

### Prerequisites
- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/)

### Setup
1. Clone the repository and navigate to the project directory.
2. (Recommended) Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```

### Running the Server
Start the Django development server:
```sh
python manage.py runserver
```
Then open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Running Tests
This project uses pytest and pytest-django for testing. To run all tests:
```sh
pytest aqform/
```
This will run unit and integration tests for form validation, API logic, and AQI result rendering.

## License
Apache 2.0
