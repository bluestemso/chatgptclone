from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI
import os
from dotenv import load_dotenv
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Chat

load_dotenv()

# Create your views here.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_openai(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    print(response)
    answer = response.choices[0].message.content
    return answer

def chatbot(request):
    chats = Chat.objects.filter(user=request.user).order_by("-created_at")
    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_openai(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html", {"chats": chats})

def login(request):
    # extract the username and password from the form and authenticate the user
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("chatbot")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")

def register(request):
    # extract the username and password from the form and create a new user
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect("chatbot")
            except:
                error_message = "An error occurred while registering your account"
                return render(request, "register.html", {"error_message": error_message})
        else:
            error_message = "Passwords do not match"
            return render(request, "register.html", {"error_message": error_message})
        
    return render(request, "register.html")

def logout(request):
    auth.logout(request)
    return redirect("login")