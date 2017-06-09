from django import forms
from django.forms import ModelForm
from models import Person
from models import SuperHeroFight


class CampingRecomendationForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'



class SubmitForm(forms.Form):
    test = forms.CharField(label='Test', max_length=100, required=False)


class SuperHeroFightForm(ModelForm):
    class Meta:
        model = SuperHeroFight
        fields = ["SuperHeroOne", "SuperHeroTwo"]



class SuperHeroFightFormEH(ModelForm):
    class Meta:
        model = SuperHeroFight

        #duration = forms.IntegerField(label="this is a test")

        fields = ["SuperHeroTwo", "home", "night", "observers", "duration"]