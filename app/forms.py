from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BlogPost
from markdownx.widgets import MarkdownxWidget

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

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
       raise forms.ValidationError("L'adresse email est déjà enregistrée.")
       
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','body','image']