from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Neighbourhoods,Profile,Message,Businesses,Comments

class BusinessForm(forms.ModelForm):
    details = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Businesses
        exclude = []
        fields = ['name','dp','details']
        
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        exclude = []
        fields = ['first_name','last_name','username','email','password1','password2']

class NeighbourhoodsForm(forms.ModelForm):
    class Meta:
        model = Neighbourhoods
        exclude = []
        fields = ['name','locale']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = []
        fields = ['comment']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fields = ['dp','bio']

class MessageForm(forms.ModelForm):
    message = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Message
        exclude = []
        fields = ['message']

class ChangeNeighbourhood(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['dp','bio','phone_number']
        fields = ['neighbourhood']
