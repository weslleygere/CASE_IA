from django import forms

class ModelTestForm(forms.Form):
    Relative_Compactness = forms.FloatField(label='Relative Compactness')
    Surface_Area = forms.FloatField(label='Surface Area')
    Wall_Area = forms.FloatField(label='Wall Area')
    Roof_Area = forms.FloatField(label='Roof Area')
    Overall_Height = forms.FloatField(label='Overall Height')
    Orientation = forms.IntegerField(label='Orientation')
    Glazing_Area = forms.FloatField(label='Glazing Area')
    Glazing_Area_Distribution = forms.IntegerField(label='Glazing Area Distribution')
