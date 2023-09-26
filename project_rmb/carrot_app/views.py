from django.contrib import auth
from django.shortcuts import render, redirect

# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'registration/login.html', {'error':'ID와 password를 확인해 주세요.'})
    return render(request, 'registration/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    return render(request, 'carrot_app/login.html')

def register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['pssword_confirm']:
            username = request.POST['username']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']

        try:
            user = UserProfile.objects.create_user(username=username, email=email password=password)
            user.last_name = last_name
            user.first_name = first_name
            user.save()
            return redirect('login')
        except Exception:
            return render(request, 'registration/register.html', {'signup_error':'password를 확인해 주세요.'})
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