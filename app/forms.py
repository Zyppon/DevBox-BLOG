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


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)
    category = forms.ChoiceField(choices=[('general-questions', 'General Questions'), ('sugestions-feedback', 'Sugestions & Feedback'),('report-bugs','Report Bugs'),('colab-partner', 'Collaborations & partnerships'), ('report-user-content', 'Report Content , Users or issues'),('others','Others...')])

