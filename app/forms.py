from django import forms
from datetime import datetime
from models.models import Event, Organization


class NewOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Organization Name'}),
        }


class LifeCycleForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'status',
        ]


class EventForm(forms.ModelForm):

    start_date_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    start_date_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=False
    )

    end_date_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=False
    )

    class Meta:
        model = Event
        fields = [
            'name',
            'event_type',
            'price',
            'short_description',
            'description',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Event Name',
                'oninput': "writeInputToSummary(event)",
                }),
            'short_description': forms.TextInput(attrs={'placeholder': 'Event Description'}),
            'description': forms.Textarea(attrs={'placeholder': 'Short Description'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data is None:
            return cleaned_data
        try:
            print("Trying to clean data")
            start_date = cleaned_data.get('start_date_date')
            start_time = cleaned_data.get('start_date_time')
            end_date = cleaned_data.get('end_date_date')
            end_time = cleaned_data.get('end_date_time')

            if start_date and start_time:
                print("combining start date and time")
                cleaned_data['start_date'] = datetime.combine(start_date, start_time)
            if end_date and end_time:
                print("combining end date and time")
                cleaned_data['end_date'] = datetime.combine(end_date, end_time)

            if (
                'start_date' in cleaned_data and
                'end_date' in cleaned_data and
                cleaned_data['end_date'] < cleaned_data['start_date']
            ):
                raise forms.ValidationError("End date must be after start date.")
            print("Data cleaned successfully")
        except Exception:
            raise forms.ValidationError("Error validating start/end date/time.")
        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.start_date = self.cleaned_data.get('start_date')
        instance.end_date = self.cleaned_data.get('end_date')

        if commit:
            instance.save()
        return instance


    def  __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.start_date:
                self.fields['start_date_date'].initial = self.instance.start_date.date()
                self.fields['start_date_time'].initial = self.instance.start_date.time()
            if self.instance.end_date:
                self.fields['end_date_date'].initial = self.instance.end_date.date()
                self.fields['end_date_time'].initial = self.instance.end_date.time()
