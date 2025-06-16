from django.shortcuts import render
from .forms import AirQualityForm
from .aq_utils import geocode_location, fetch_air_quality

import requests

def air_quality_form(request):
    context = {}
    if request.method == 'POST':
        form = AirQualityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country'] or 'USA'
            lat, lon, display_name = geocode_location(city, state, country)
            if not lat or not lon:
                context['error'] = 'Location not found. Please check your input.'
            else:
                aq_data = fetch_air_quality(lat, lon)
                if not aq_data or 'hourly' not in aq_data or 'us_aqi' not in aq_data['hourly']:
                    context['error'] = 'Could not fetch air quality data. Please try again later.'
                else:
                    # Get the latest AQI value and details
                    aqi_list = aq_data['hourly']['us_aqi']
                    time_list = aq_data['hourly']['time']
                    if aqi_list:
                        latest_idx = len(aqi_list) - 1
                        context['aqi'] = aqi_list[latest_idx]
                        context['measurement_time'] = time_list[latest_idx]
                        # Find main pollutant (highest AQI component)
                        main_pollutant, main_value = None, -1
                        for pollutant in ['us_aqi_pm2_5','us_aqi_pm10','us_aqi_o3','us_aqi_no2','us_aqi_so2','us_aqi_co']:
                            if pollutant in aq_data['hourly']:
                                val = aq_data['hourly'][pollutant][latest_idx]
                                if val is not None and val > main_value:
                                    main_value = val
                                    main_pollutant = pollutant
                        context['main_pollutant'] = main_pollutant
                        context['display_name'] = display_name
                        # Simple health advisory
                        if context['aqi'] <= 50:
                            context['advisory'] = 'Good air quality.'
                        elif context['aqi'] <= 100:
                            context['advisory'] = 'Moderate air quality.'
                        elif context['aqi'] <= 150:
                            context['advisory'] = 'Unhealthy for sensitive groups.'
                        elif context['aqi'] <= 200:
                            context['advisory'] = 'Unhealthy.'
                        elif context['aqi'] <= 300:
                            context['advisory'] = 'Very unhealthy.'
                        else:
                            context['advisory'] = 'Hazardous.'
                    else:
                        context['error'] = 'No AQI data available.'
        context['form'] = form
    else:
        context['form'] = AirQualityForm()
    return render(request, 'aqform/form.html', context)
