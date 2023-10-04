from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Post, StandardArea
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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
    return render(request, 'carrot_app/search.html')

# 동네인증 화면
@login_required
def location(request):
    try:
        user_profile = UserProfile.objects.get(user_id=request.user)
        region = user_profile.region
    except UserProfile.DoesNotExist:
        region = None

    return render(request, 'carrot_app/location.html', {'region': region})

def trade(request):
    return render(request, 'carrot_app/trade.html')

def trade_post(request):
    return render(request, 'carrot_app/trade_post.html')

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

# 지역설정
@login_required
def set_region(request):
    if request.method == "POST":
        region_name = request.POST.get('region-setting')

        if region_name:
            try:
                # StandardArea 모델에서 입력된 지역명에 해당하는 인스턴스를 가져옴
                region_instance, created = StandardArea.objects.get_or_create(area_name=region_name)

                # 현재 로그인한 사용자의 프로필을 가져오거나 생성
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)

                # UserProfile의 region 필드에 해당 인스턴스를 할당
                user_profile.region = region_instance
                user_profile.region_certification = 'Y'  # 동네 인증 완료
                user_profile.save()

                return JsonResponse({"status": "success", "message": "동네 인증이 완료되었습니다."})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        else:
            return JsonResponse({"status": "error", "message": "지역을 입력하세요."})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

# 지역인증 완료
@login_required
def set_region_certification(request):
    if request.method == "POST":
        request.user.profile.region_certification = 'Y'
        request.user.profile.save()
        messages.success(request, "인증되었습니다")
        return redirect('carrot_app:location')