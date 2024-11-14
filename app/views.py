from http.client import responses

from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

import os
from dotenv import load_dotenv

load_dotenv()

# Create your views here.
gemini_api_key = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=gemini_api_key)


def ask_gemini(message):
    model = genai.GenerativeModel("gemini-1.5-flash-8b-001")
    response = model.generate_content(message)
    return response.text
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get('message')
        response = ask_gemini(message)
        return JsonResponse({'message':message,'response':response})
    return render(request,'app/chatbot.html')