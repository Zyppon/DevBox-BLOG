from django.shortcuts import  render, redirect , get_object_or_404
from django.contrib.auth import authenticate ,login
from django.contrib import messages
from .forms import NewUserForm , LoginForm , PostForm , PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import BlogPost , VerificationCode
import random
import string
from django.core.mail import send_mail
from django.conf import settings

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes 
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse



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
        if form.is_valid(): # Salvează utilizatorul în baza de date
            username = form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1') 
            user = authenticate(request, username=username, email=email , password=password)
            user = form.save(commit=False)  # Salvăm utilizatorul fără a-l comite în baza de date încă
            user.is_active = False  # Setăm utilizatorul ca inactiv până când confirmă prin email
            user.save()

            token_generator = default_token_generator
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            # Construim URL-ul pentru activarea contului
            current_site = get_current_site(request)
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

            # Construim mesajul de email pentru activarea contului
            
            email_subject = 'Activate your account'
            email_message = render_to_string('authentificate/account_activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            extract_html_message = strip_tags(email_message)
            send_mail(
                email_subject,
                extract_html_message,
                settings.EMAIL_HOST_USER,  # Adresa ta de email
                [email],  # Adresa de email a utilizatorului
                fail_silently=False,
            )
            messages.success(request, "Registered successfully. Check your email for activation link.")
            return redirect('login') 
    else:
        form = NewUserForm()

    return render(request, 'authentificate/register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decodifică uidb64
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Activarea contului
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been successfully activated. Please log in.")
        return redirect('login')
    else:
        # Token invalid sau utilizator inexistent
        messages.error(request, "Invalid activation link.")
        return redirect('login')

@login_required
def home(request):
    if not request.user.is_active:
        # Utilizatorul nu a verificat contul, deci redirecționează-l către o altă pagină sau afișează un mesaj de eroare
        messages.error(request, "Your account is not activated. Please activate your account first.")
        return redirect('login')  # Redirecționează către o altă pagină care afișează un mesaj sau instrucțiuni pentru activare
    else:
        # Utilizatorul este autentificat și contul este activat, deci afișează pagina de home normal
        return render(request, 'index.html')


#def reset_password(request, uidb64, token):
    #if request.method == 'POST':
        #form = PasswordResetForm(request.POST)
        #if form.is_valid():
           # email = form.cleaned_data.get('email')
            # Verifică dacă adresa de email există în baza de date
           # if User.objects.filter(email=email).exists():
               # reset_link = request.build_absolute_uri('/reset_password/{}/{}/'.format(uidb64, token))
               # subject = 'DevBox Reset Password'
               # message = render_to_string('authentificate/reset.txt', {'reset_link': reset_link})
               # send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                # Redirect către o pagină care confirmă trimiterea email-ului de resetare
               # return render(request, 'authentificate/password_reset_confirmation.html')
           # else:
                # Adresa de email nu există în baza de date
                # Afișează un mesaj de eroare pe aceeași pagină sau gestionează în alt mod
               # return render(request, 'authentificate/password_reset.html', {'form': form, 'error_message': "Email doesn't exist."})
   # else:
      #  form = PasswordResetForm()
    # Returnează pagina de resetare a parolei pentru metoda GET
  #  return render(request, 'authentificate/password_reset.html', {'form': form})




def logout(request):
    auth.logout(request)
    messages.info(request ,'Vous avez été déconnecté.')
    return redirect("index")
  


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST , request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'blog_post/add_post.html', {'form': form})


def blog_detail(request , post_id):
    post = get_object_or_404(BlogPost , id=post_id)
    return render(request , 'blog_post/blog_detail.html' , {'post':post})

def user_settings_panel(request):
    return render(request , 'authentificate/user_settings.html')

def courses_download(request):
    return render(request , 'courses.html')