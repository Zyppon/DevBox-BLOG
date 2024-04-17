from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import BlogPost
from markdownx.widgets import MarkdownxWidget
from django.contrib.auth.forms import PasswordChangeForm



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

class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
       # email = cleaned_data.get("email")

        if not username:
            raise forms.ValidationError("At least one field must be filled.")

        if username:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("A user with this username already exists.")
        
       # if email:
           # if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
              #  raise forms.ValidationError("A user with this email already exists.")

        return cleaned_data
       
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


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    def clean_old_password(self):
        """
        Validate that the old password is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your old password was entered incorrectly. Please enter it again.")
        return old_password

class NewsForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','body']