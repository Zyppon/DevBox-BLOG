
from django.shortcuts import render

def index(request):
  return render(request , 'index.html')

def privacy(request):
  return render(request , 'privacy.html')

def login(request):
  return render(request , 'login.html')

