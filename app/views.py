from django.shortcuts import  render, redirect , get_object_or_404
from django.contrib.auth import authenticate ,login ,update_session_auth_hash
from django.contrib import messages
from .forms import NewUserForm , LoginForm , PostForm , PasswordResetForm , ContactForm , UserSettingsForm , PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import BlogPost , NewsPost
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


from django.core.mail import EmailMultiAlternatives , EmailMessage
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

import cloudinary
from cloudinary.uploader import upload
from cloudinary.models import CloudinaryResource

from django.db.models import Q

def index(request):

  search_post = request.GET.get('search')

  if search_post:
      posts = BlogPost.objects.filter(Q(title__icontains=search_post))
  else:
      posts = BlogPost.objects.all()

  return render(request , 'index.html' , {'posts':posts , 'search_query': search_post})

def about_us(request):
    return render(request , 'about_us.html')

def news(request):
    news_post  = NewsPost.objects.all()
    return render(request , 'news.html' , {'news_post': news_post})

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
           messages.error(request, "Email or password incorrect.")
           
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
            
            email_subject = 'DevBox - Activate Your Account'
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
            messages.success(request, "Successfully recorded. Check your email for the activation link. ")
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
        # Account Activation
         
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been successfully activated. Please log in.")
        return redirect('login')
    else:
        # Token non valide ou utilisateur inexistant
        messages.error(request, "Invalid activation link.")
        return redirect('login')

#@login_required
def home(request):
    if not request.user.is_active:
        messages.error(request, "Your account isn't activated. Veuillez d'abord activer votre compte.")
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
                messages.success(request, "Your password has been reset successfully.")
                return redirect('reset_password_done')
            else:
                messages.error(request, "Passwords don't match. Please try again.")
        return render(request, 'authentificate/resetpassword/reset_password_confirm.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "The password reset link is invalid. Please request a new one.")
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
            messages.success(request, "An email has been sent to your inbox.")
        else:
            messages.error(request, "This e-mail is not saved in our database. Please try again.")
    return render(request, 'authentificate/resetpassword/password_reset.html')



def logout(request):
    auth.logout(request)
    messages.info(request ,"You've been logged out.")
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



@login_required(login_url='login')
def update_post(request):
    if request.method == 'POST':
        if 'delete_post' in request.POST:
              # Delete Post
            try:

                post_id = request.POST.get('delete_post')

                post = get_object_or_404(BlogPost, id=post_id)

                if post.image:
                    # Obtain Public Id Image from Cloudinary
                    public_id = post.image.public_id

                    # Delete Image From Cloudinary
                    cloudinary.uploader.destroy(public_id)

                post.delete()

                messages.success(request, 'Your post has been deleted successfully.')

                return redirect('update_post')
            except BlogPost.DoesNotExist:

                # In case the post does not exist, display an error message

                messages.error(request, 'Error deleting post: No BlogPost matches the given query.')

                return redirect('update_post')

            except Exception as e:

                # In case of error, display an error message

                messages.error(request, f'Error deleting post: {str(e)}')

                return redirect('update_post')
    current_user = request.user
    posts = BlogPost.objects.filter(author=current_user)
    return render(request , 'blog_post/update_post.html' , {'posts':posts})

@login_required(login_url='login')
def edit_post_view(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.user != post.author:
        messages.error(request , "You can't edit Blog Posts from another user")
        return redirect('index')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Add request.FILES for updating images 
        if form.is_valid():
            # Save form without save in database
            new_post = form.save(commit=False)
            # Verify if image has been uploaded
            if 'image' in request.FILES:
                # Update image in Cloudinary
                
                # If Old image exist, delete from Cloudinary

                new_image_url = cloudinary.uploader.upload(request.FILES['image']).get('secure_url')
                # Update image input with new url image
                
                new_post.image = new_image_url
            
            # Save in data base
            new_post.save()
            
            messages.success(request, 'Your Post Has Been Updated Successfully.')
            return redirect(reverse('update_post'))  
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog_post/edit_post_view.html', {'form': form})


#@login_required(login_url='login')
#def user_settings(request):
    #if request.method == 'POST':
        #user_form = UserSettingsForm(request.POST, instance=request.user)
        #if user_form.is_valid():
            #username = user_form.cleaned_data['username']
           # email = user_form.cleaned_data['email']
            
            #if User.objects.filter(email=email).exclude(pk=request.user.pk).exists() or \
              # User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
              #  messages.error(request, 'Email or Username Already Exists')
           # else:
              #  user_form.save()
              #  messages.success(request, 'Profile updated successfully!')
                
   # else:
   #     user_form = UserSettingsForm(instance=request.user)
  #  return render(request, 'authentificate/user_settings.html', {'user_form': user_form})

@login_required(login_url='login')
def user_settings(request):
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            # Delete user and log out
            try:
                request.user.delete()
                logout(request)
                messages.success(request, 'Your account Has Been Deleted With Succes')
                delete_email(request)
                return redirect('login')
            except Exception as e:
                # In case of error, display an error message
                messages.error(request, f'Error for erase your account: {str(e)}')
                return redirect('user_settings')
        
        # If it is not an account deletion request, treat the profile update
        user_form = UserSettingsForm(request.POST, instance=request.user)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            user = user_form.save(commit=False)
            user.username = username
            user.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Invalid form data. Please correct the errors and try again.')
    
    else:
        user_form = UserSettingsForm(instance=request.user)
    
    return render(request, 'authentificate/user_settings.html', {'user_form': user_form})


#def delete_user(user):
    #try:
        #user.delete()
        #return True, "Utilisateur supprimé avec succès."
    #except Exception as e:
        #return False, f"Une erreur s'est produite lors de la suppression de l'utilisateur : {str(e)}"


def confirm_email(request  , token , ui):
    email = user_form.cleaned_data['email']
    if request.method == 'POST':
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(request.user.pk))
        token = token_generator.make_token(request.user)
        subject = 'Email Confirmation'
        message = f'Click this link to confirm your email address: {request.build_absolute_uri(reverse("confirm_email", kwargs={"uidb64": uid, "token": token}))}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    else:
        messages.error(request , 'The Link is not valid or expired')

    return render(request, 'authentificate/user_settings.html')




def courses_download(request):
    return render(request , 'courses.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            category = form.cleaned_data['category']
            subject = f"Contact - {category} from {name}"
            EmailMessage(
               subject,
               message,
               email, # Send from (your website)
               [settings.EMAIL_HOST_USER], # Send to (your admin email)
               [],
               reply_to=[email] # Email from the form to get back to
           ).send()
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('change_password')
        else:

            messages.error(request, "Your Old Password Is Incorrect or new passrword didn't match")

    else:

        form = PasswordChangeForm(user=request.user)
    return render(request , 'authentificate/changepassword/change_password.html' , {'form':form})

