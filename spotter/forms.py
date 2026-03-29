from django import forms
from .models import Card, User
from django.contrib.auth.forms import UserCreationForm

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['problem', 'goal']
        widgets = {
            'problem': forms.Textarea(attrs={'rows': 3}),
            'goal': forms.Textarea(attrs={'rows': 3}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role')