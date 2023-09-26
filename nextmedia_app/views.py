
from django.shortcuts import render
from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate ,login
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserForm
from django.contrib.auth import logout


def index(request):
  return render(request , 'index.html')

def privacy(request):
  return render(request , 'privacy.html')

def login_user(request):
  return render(request , 'authentificate/login.html')

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1'] 
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Registered successfully")
            return redirect('index')
    else:
        form = NewUserForm()

    return render(request, 'authentificate/register.html', {'form': form})
  
def logout_view(request):
    logout(request)
    return redirect('index')
  

