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
from django.utils.encoding import force_bytes , force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


from cloudinary.uploader import upload


def index(request):
  posts = BlogPost.objects.all()
  return render(request , 'index.html' , {'posts':posts})

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
            email_subject_login = 'DevBox - Thanks For logging Back.'
            email_message_login = render_to_string('authentificate/account_login_email.html', {
                'user': user,
                
            })

            extract_login_message = strip_tags(email_message_login)
            send_mail(
                email_subject_login,
                extract_login_message,
                settings.EMAIL_HOST_USER, 
                [email],  
                fail_silently=False,
            )
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
            username = form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1') 
            user = authenticate(request, username=username, email=email , password=password)
            user = form.save(commit=False)  # Nous enregistrons l'utilisateur sans l'inscrire encore dans la base de données
            user.is_active = False  # Nous définissons l'utilisateur comme inactif jusqu'à ce qu'il confirme par e-mail
            user.save()

            token_generator = default_token_generator
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            # Nous construisons l'URL pour l'activation du compte
            current_site = get_current_site(request)
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

            # Nous construisons le message pour l'activation du compte
            
            email_subject = 'DevBox - Activez votre compte'
            email_message = render_to_string('authentificate/account_activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            extract_html_message = strip_tags(email_message)
            send_mail(
                email_subject,
                extract_html_message,
                settings.EMAIL_HOST_USER,  # Votre adresse du EMail pour HOST
                [email],  # L'adrese du utilisateur
                fail_silently=False,
            )
            messages.success(request, "Enregistré avec succès. Vérifiez votre e-mail pour le lien d'activation.")
            return redirect('login') 
    else:
        form = NewUserForm()

    return render(request, 'authentificate/register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decodification uidb64
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Activation du Compte
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a été activé avec succès. Veuillez vous connecter.")
        return redirect('login')
    else:
        # Token non valide ou utilisateur inexistant
        messages.error(request, "Invalid activation link.")
        return redirect('login')

@login_required
def home(request):
    if not request.user.is_active:
        messages.error(request, "Votre compte n'est pas activé. Veuillez d'abord activer votre compte.")
        return redirect('login')  
    else:
        
        return render(request, 'index.html')


def reset_password_done(request):
    return render(request , 'authentificate/resetpassword/reset_password_done.html')

def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Processing Password
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
                return redirect('reset_password_done')
            else:
                messages.error(request, "Les mots de passe ne correspondent pas. Veuillez réessayer.")
        return render(request, 'authentificate/resetpassword/reset_password_confirm.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "Le lien de réinitialisation du mot de passe n'est pas valide. Veuillez en demander un nouveau.")
        return redirect('index') 



def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(f'/reset_password_confirm/{urlsafe_base64_encode(force_bytes(user.pk))}/{token}/')
            subject = "DevBox Reset Password"
            message = render_to_string('authentificate/resetpassword/reset.html' , {'reset_link': reset_link})
            extract_reset_message = strip_tags(message)
            send_mail(subject, extract_reset_message, settings.EMAIL_HOST_USER, [email])
            messages.success(request, "Un e-mail a été envoyé dans votre boîte de réception.")
        else:
            messages.error(request, "Cet e-mail n'est pas enregistré dans notre base de données. Veuillez réessayer.")
    return render(request, 'authentificate/resetpassword/password_reset.html')



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

def privacy(request):
    return render(request , 'privacy.html')