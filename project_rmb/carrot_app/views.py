from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Post
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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

def register(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            try:
                user = User.objects.create_user(username=username, password=password)
                return redirect('login')
            except Exception:
                error_message = '회원가입 중 오류가 발생했습니다.'
        else:
            error_message = '비밀번호와 비밀번호 확인이 일치하지 않습니다.'

    return render(request, 'registration/register.html', {'error_message': error_message})

def main(request):
    return render(request, 'carrot_app/main.html')

def search(request):
    query = request.GET.get('search')
    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    else:
        results = Post.objects.all()
    
    return render(request, 'carrot_app/search.html', {'posts': results})

# 동네인증 화면
@login_required
def location(request):
    try:
        user_profile = UserProfile.objects.get(user_id=request.user)
        region = user_profile.region
    except UserProfile.DoesNotExist:
        region = None

    return render(request, 'carrot_app/location.html', {'region': region})

# 중고거래 화면
def trade(request):
    top_views_posts = Post.objects.filter(status='판매중').order_by('-view_num')
    return render(request, 'carrot_app/trade.html', {'posts': top_views_posts})

# 중고거래상세정보(각 포스트) 화면
def trade_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 조회수 증가
    if request.user.is_authenticated:
        if request.user != post.user:
            post.view_num += 1
            post.save()
    else:
        post.view_num += 1
        post.save()

    try:
        user_profile = UserProfile.objects.get(user=post.user)
    except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'post': post,
        'user_profile': user_profile
    }

    return render(request, 'carrot_app/trade_post.html', context)

# alert용 화면
def alert(request, alert_message):
    return render(request, 'carrot_app/alert.html', {'alert_message': alert_message})

@login_required
def write(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
        if user_profile.region_certification == 'Y':
            return render(request, 'carrot_app/write.html')
        else:
            return redirect('carrot_app:alert', alert_message='동네인증이 필요합니다.')
    except UserProfile.DoesNotExist:
        return redirect('carrot_app:alert', alert_message='동네인증이 필요합니다.')

def edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post:
        post.description = post.description.strip()
    if request.method == "POST":
        post.title = request.POST['title']
        post.price = request.POST['price']
        post.description = request.POST['description']
        post.location = request.POST['location']
        if 'images' in request.FILES:
            post.images = request.FILES['images']
        post.save()
        return redirect('carrot_app:trade_post', pk=id)

    return render(request, 'carrot_app/write.html', {'post': post})

@login_required
def chat(request):
    return render(request, 'carrot_app/chat.html')

def index(request):
    return render(request, 'carrot_app/index.html')

def create_form(request):
    return render(request, 'carrot_app/create_form.html')