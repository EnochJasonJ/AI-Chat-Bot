from http.client import responses
import os
from dotenv import load_dotenv
from django.shortcuts import render , redirect
from django.http import JsonResponse
import google.generativeai as genai
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from .models import chats
import re
from django.utils.html import escape
# Create your views here.
load_dotenv()
gemini_api_key = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)
genai.configure(api_key="AIzaSyBdNNLAMqq95zJ5sj8bAGyDl1sApcVqrzs")


def ask_gemini(message):
    model = genai.GenerativeModel("gemini-1.5-flash-8b-001")
    response = model.generate_content(message)
    return response.text





def chatbot(request):
    if request.user.is_authenticated:
        Chats = chats.objects.filter(user = request.user)
    else:
        Chats = None
    if request.method == "POST":
        message = request.POST.get('message')
        response = ask_gemini(message)
        chat = chats(user = request.user,message=message,response=response,created_at = timezone.now)
        chat.save()
        return JsonResponse({'message':message,'response':response})
    return render(request,'app/chatbot.html',{'Chats':Chats})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid Username or Password'
            return render(request,'app/login.html',{'error_message': error_message})
    return render(request,'app/login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_message = 'Error in creating your account.'
                return render(request,'app/register.html',{'error_message':error_message})
        else:
            error_message = 'Password Does Not Match'
            return render(request,'app/register.html',{'error_message':error_message})
    return render(request,'app/register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')