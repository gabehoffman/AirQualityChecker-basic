from django import forms

class AirQualityForm(forms.Form):
    city = forms.CharField(label='City', max_length=100, required=True)
    state = forms.CharField(label='State/Province/Region', max_length=100, required=True)
    country = forms.CharField(label='Country', max_length=100, required=False, initial='USA')

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        country = cleaned_data.get('country')
        if not city or not state:
            raise forms.ValidationError('City and State/Province/Region are required.')
        if not country:
            cleaned_data['country'] = 'USA'
        return cleaned_data
