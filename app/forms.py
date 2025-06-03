from django import forms
from models.models import Event, Organization

class NewOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Organization Name'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'event_type',
            'start_date',
            'end_date',
            'price',
            'description',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Event Name',
                'oninput': "writeInputToSummary(event)",
                }),
            'description': forms.Textarea(attrs={'placeholder': 'Event Description'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        try:
            assert cleaned_data is not None
            start = cleaned_data.get('start_date')
            end = cleaned_data.get('end_date')
        except AssertionError:
            raise forms.ValidationError("Start and end dates are required.")


        if start and end and end < start:
            raise forms.ValidationError("End date must be after start date.")

