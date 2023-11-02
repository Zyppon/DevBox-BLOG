from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
   # username = forms.CharField(label='Username', max_length=15, required=True, initial='')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def clean_email(self):
       email = self.cleaned_data.get('email')
       try:
           match = User.objects.get(email=email)
       except User.DoesNotExist:
           return email
       raise forms.ValidationError('Email address already registered.')
       
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)