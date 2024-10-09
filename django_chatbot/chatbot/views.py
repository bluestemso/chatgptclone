from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_openai(message):
    response = client.completions.create(model="davinci-002",
    prompt=message,
    max_tokens=150,
    n=1,
    stop=None,
    temperature=0.7)
    print(response)
    answer = response.choices[0].text.strip()
    return answer

# Create your views here.
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_openai(message)
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html")