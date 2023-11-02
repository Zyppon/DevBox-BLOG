
from django.shortcuts import render
from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate ,login
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserForm , LoginForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.http import HttpResponse

def index(request):
  return render(request , 'index.html')

def privacy(request):
  return render(request , 'privacy.html')

#def login_user(request):
   # if request.method == "POST":
     #   form = NewUserForm(request.POST)  # Creați o instanță a formularului de înregistrare
     #   if form.is_valid():
        #    email = form.cleaned_data['email']
         #   password = form.cleaned_data['password']
        #    user = authenticate(request, email=email, password=password)
         #   if user is not None and check_password(password, user.password):
          #      login(request, user)
                # Redirecționați la o altă pagină după autentificare cu succes
         #       return redirect(settings.LOGIN_REDIRECT_URL)
         #   else:
          #      messages.error(request, 'Invalid Email or Password')
  #  else:
   #     form = NewUserForm()

#    return render(request, 'authentificate/login.html', {'form': form})

#def login(request):
    #if request.method == 'POST':

        #email = request.POST.get('email')
        #password = request.POST.get('password2')
        #user = auth.authenticate(request, email=email, password=password)
        #if user is not None and user.check_password(password):
            #auth.login(request, user)    
            #return redirect('index')
        #else:
            #messages.error(request , "Invalid Email or Password.")
        
    #return render(request, 'authentificate/login.html' , {'form':LoginForm})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password2 = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            
        except User.DoesNotExist:
            user = None
            

        if user is not None and  user.check_password(password2):
            auth.login(request, user)
            return redirect('index')
        else:
           messages.error(request, "Invalid Email or Password.")
          # error_message = "Invalid Email or Password."
    else:
        form = LoginForm()
    return render(request, 'authentificate/login.html' , {'form':LoginForm})

  
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
  
def logout(request):
    auth.logout(request)
    messages.info(request ,'You have been logged out.')
    return redirect("index")
  

