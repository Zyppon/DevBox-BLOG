from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate ,login
from django.contrib import messages
from .forms import NewUserForm , LoginForm
from django.contrib.auth.models import User
from django.contrib import auth

def index(request):
  return render(request , 'index.html')

def privacy(request):
  return render(request , 'privacy.html')

def login_user(request):
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
           messages.error(request, "Email ou mot de passe invalide.")
    else:
        form = LoginForm()
    return render(request, 'authentificate/login.html' , {'form':LoginForm})

  
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') 
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Enregistré avec succès")
            return redirect('login')
    else:
        form = NewUserForm()

    return render(request, 'authentificate/register.html', {'form': form})
  
def logout(request):
    auth.logout(request)
    messages.info(request ,'Vous avez été déconnecté.')
    return redirect("index")
  

