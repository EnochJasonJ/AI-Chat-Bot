from http.client import responses

from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

# Create your views here.

genai.configure(api_key="AIzaSyBdNNLAMqq95zJ5sj8bAGyDl1sApcVqrzs")


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