from django.urls import path
from aqform.views import air_quality_form

urlpatterns = [
    path('', air_quality_form, name='air_quality_form'),
]