from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Post, StandardArea
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from .forms import PostForm

from .models import UserProfile, Post, ChatRoom, ChatMessage

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
            return redirect('alert', alert_message='동네인증이 필요합니다.')
    except UserProfile.DoesNotExist:
        return redirect('alert', alert_message='동네인증이 필요합니다.')

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


# 포스트 업로드
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # 임시 저장
            post.user = request.user  # 작성자 정보 추가 (이 부분을 수정했습니다)
            post.save()  # 최종 저장
            return redirect('carrot_app:trade_post', pk=post.pk)  # 저장 후 상세 페이지로 이동
    else:
        form = PostForm()
    return render(request, 'carrot_app/trade_post.html', {'form': form})

# 지역설정
@login_required
def set_region(request):
    if request.method == "POST":
        region_full = request.POST.get('region-setting')  # 전체 지역명 입력값 가져오기

        if region_full:
            try:
                # 공백을 기준으로 지역명과 시/도명을 분리
                region_parts = region_full.split(' ')
                
                if len(region_parts) >= 2:
                    city_name = region_parts[0]  # 첫 번째 단어를 city_name으로 저장
                    area_name = ' '.join(region_parts[1:])  # 나머지 부분을 area_name으로 저장

                    # StandardArea 모델에서 입력된 지역명에 해당하는 인스턴스를 가져옴
                    region_instance, created = StandardArea.objects.get_or_create(area_name=area_name)

                    # city_name과 area_name을 할당
                    region_instance.city_name = city_name
                    region_instance.save()

                    # 현재 로그인한 사용자의 프로필을 가져오거나 생성
                    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

                    # UserProfile의 region 필드에 해당 인스턴스를 할당
                    user_profile.region = region_instance
                    user_profile.region_certification = 'Y'  # 동네 인증 완료
                    user_profile.save()

                    return redirect('carrot_app:location')
                else:
                    return JsonResponse({"status": "error", "message": "올바른 형식으로 지역을 입력하세요."})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        else:
            return JsonResponse({"status": "error", "message": "지역을 입력하세요."})
    else:
        # GET 요청의 경우 HttpResponse 객체 반환
        return HttpResponse("GET request received. This view is for POST requests only.", status=405)

# 지역인증 완료
@login_required
def set_region_certification(request):
    if request.method == "POST":
        request.user.profile.region_certification = 'Y'
        request.user.profile.save()
        messages.success(request, "인증되었습니다")
        return redirect('carrot_app:location')