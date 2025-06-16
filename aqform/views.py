from django.shortcuts import render
from .forms import AirQualityForm

def air_quality_form(request):
    if request.method == 'POST':
        form = AirQualityForm(request.POST)
        if form.is_valid():
            # For now, just re-render the form with a success message
            return render(request, 'aqform/form.html', {'form': form, 'success': True})
    else:
        form = AirQualityForm()
    return render(request, 'aqform/form.html', {'form': form})
