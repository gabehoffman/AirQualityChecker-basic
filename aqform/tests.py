import pytest
from django.urls import reverse
from aqform.forms import AirQualityForm
from aqform import aq_utils
from unittest.mock import patch

@pytest.mark.django_db
def test_form_valid_data():
    form = AirQualityForm(data={
        'city': 'New York',
        'state': 'NY',
        'country': 'USA',
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_form_missing_city():
    form = AirQualityForm(data={
        'city': '',
        'state': 'NY',
        'country': 'USA',
    })
    assert not form.is_valid()
    assert 'city' in form.errors or form.non_field_errors()

@pytest.mark.django_db
def test_form_missing_state():
    form = AirQualityForm(data={
        'city': 'New York',
        'state': '',
        'country': 'USA',
    })
    assert not form.is_valid()
    assert 'state' in form.errors or form.non_field_errors()

@patch('aqform.aq_utils.requests.get')
def test_geocode_location_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{
        'lat': '40.7128', 'lon': '-74.0060', 'display_name': 'New York, NY, USA'
    }]
    lat, lon, name = aq_utils.geocode_location('New York', 'NY', 'USA')
    assert lat == '40.7128'
    assert lon == '-74.0060'
    assert 'New York' in name

@patch('aqform.aq_utils.requests.get')
def test_geocode_location_not_found(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []
    lat, lon, name = aq_utils.geocode_location('FakeCity', 'ZZ', 'Nowhere')
    assert lat is None and lon is None and name is None

@patch('aqform.aq_utils.requests.get')
def test_fetch_air_quality_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'hourly': {
            'us_aqi': [42],
            'time': ['2025-06-16T12:00'],
            'us_aqi_pm2_5': [42],
        }
    }
    data = aq_utils.fetch_air_quality('40.7128', '-74.0060')
    assert data['hourly']['us_aqi'][0] == 42

@patch('aqform.aq_utils.requests.get')
def test_fetch_air_quality_failure(mock_get):
    mock_get.side_effect = Exception('API error')
    data = aq_utils.fetch_air_quality('40.7128', '-74.0060')
    assert data is None

@patch('aqform.aq_utils.fetch_air_quality', return_value={
    'hourly': {
        'us_aqi': [42],
        'time': ['2023-10-01T12:00:00Z'],
        'us_aqi_pm2_5': [42],
    }
})
@patch('aqform.aq_utils.geocode_location', return_value=('40.7128', '-74.0060', 'New York, NY, USA'))
def test_integration_form_and_view(mock_geocode, mock_fetch_air_quality, client):
    url = reverse('air_quality_form')
    response = client.post(url, {'city': 'New York', 'state': 'NY', 'country': 'USA'})

    assert response.status_code == 200
    assert '<p><strong>AQI:</strong> 42</p>' in response.content.decode()
    assert '<p><strong>Main Pollutant:</strong> us_aqi_pm2_5</p>' in response.content.decode()
    assert '<p><strong>Measurement Time:</strong> 2023-10-01T12:00:00Z</p>' in response.content.decode()
    assert '<p><strong>Health Advisory:</strong> Good air quality.</p>' in response.content.decode()
