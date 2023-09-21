from django.shortcuts import render, redirect

# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

def register(request):
    return render(request, 'registration/register.html')

def main(request):
    return render(request, 'carrot_app/main.html')

def search(request):
    return render(request, 'carrot_app/search.html')

def location(request):
    return render(request, 'carrot_app/location.html')

def trade(request):
    return render(request, 'carrot_app/trade.html')

def trade_post(request):
    return render(request, 'carrot_app/trade_post.html')

def write(request):
    return render(request, 'carrot_app/write.html')

def chat(request):
    return render(request, 'carrot_app/chat.html')

def index(request):
    return render(request, 'carrot_app/index.html')

def create_form(request):
    return render(request, 'carrot_app/create_form.html')