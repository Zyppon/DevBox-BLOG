from django.shortcuts import  render, redirect , get_object_or_404
from django.contrib.auth import authenticate ,login
from django.contrib import messages
from .forms import NewUserForm , LoginForm , PostForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import BlogPost



def index(request):
  posts = BlogPost.objects.all()
  return render(request , 'index.html' , {'posts':posts})

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
  


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm()

    return render(request, 'blog_post/add_post.html', {'form': form})


def blog_detail(request , post_id):
    post = get_object_or_404(BlogPost , id=post_id)
    return render(request , 'blog_post/blog_detail.html' , {'post':post})

