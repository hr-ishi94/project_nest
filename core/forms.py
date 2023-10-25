# forms.py
from django import forms

class PriceRangeForm(forms.Form):
    min_price = forms.FloatField()  # Adjust the field type as needed
    max_price = forms.FloatField()  # Adjust the field type as needed
