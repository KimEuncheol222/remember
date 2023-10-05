from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import View
from .forms import PostForm

from .models import UserProfile, Post, StandardArea, ChatRoom, Message

# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('carrot_app:main')
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
                return redirect('carrot_app:login')
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
def alert(request, alert_message, redirect_url='location'):
    context = {
        'alert_message': alert_message,
        'redirect_url': redirect_url
    }
    return render(request, 'carrot_app/alert.html', context)

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



# 채팅 ################################################################################

def chat(request):
    return render(request, 'carrot_app/chat.html')

# 채팅테스트

def index(request): 
    return render(request, 'carrot_app/chat_index.html')


# 채팅방 열기
def chat_room(request, pk):
    user = request.user
    chat_room = get_object_or_404(ChatRoom, pk=pk)

    # 내 ID가 포함된 방만 가져오기
    chat_rooms = ChatRoom.objects.filter(
            Q(receiver_id=user) | Q(starter_id=user)
        ).order_by('-latest_message_time')  # 최신 메시지 시간을 기준으로 내림차순 정렬
    
    # 각 채팅방의 최신 메시지를 가져오기
    chat_room_data = []
    for room in chat_rooms:
        latest_message = Message.objects.filter(chatroom=room).order_by('-timestamp').first()
        if latest_message:
            chat_room_data.append({
                'chat_room': room,
                'latest_message': latest_message.content,
                'timestamp': latest_message.timestamp,
            })

    # 상대방 정보 가져오기
    if chat_room.receiver == user:
        opponent = chat_room.starter
    else:
        opponent = chat_room.receiver

    opponent_user = User.objects.get(pk=opponent.pk)


    # post의 상태 확인 및 처리
    if chat_room.post is None:
        seller = None
        post = None
    else:
        seller = chat_room.post.user
        post = chat_room.post

    return render(request, 'carrot_app/chat_room.html', {
        'chat_room': chat_room,
        'chat_room_data': chat_room_data,
        'room_name': chat_room.pk,
        'seller': seller,
        'post': post,
        'opponent': opponent_user,
    })


# 채팅방 생성 또는 참여
def create_or_join_chat(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    chat_room = None
    created = False

    # 채팅방이 이미 존재하는지 확인
    chat_rooms = ChatRoom.objects.filter(
        Q(starter=user, receiver=post.user, post=post) |
        Q(starter=post.user, receiver=user, post=post)
    )
    if chat_rooms.exists():
        chat_room = chat_rooms.first()
    else:
        # 채팅방이 존재하지 않는 경우, 새로운 채팅방 생성
        chat_room = ChatRoom(starter=user, receiver=post.user, post=post)
        chat_room.save()
        created = True
        post.chat_num += 1
    
    # 새로운 채팅방을 만든 후 해당 채팅방으로 리디렉션
    return redirect('carrot_app:chat_room', pk=chat_room.pk)


# 가장 최근 채팅방 가져오기
@login_required
def get_latest_chat(request, pk):
    user = request.user
    # 1) 해당 pk인 채팅방 중 가장 최신 채팅방으로 리디렉션
    try:
        latest_chat_with_pk = ChatRoom.objects.filter(
            Q(post_id=pk) &
            (Q(receiver=user) | Q(starter=user))
        ).latest('latest_message_time')
        return redirect('carrot_app:chat_room', pk=latest_chat_with_pk.room_number)
    
    except ChatRoom.DoesNotExist:
        pass

    # 2) 위 경우가 없다면 내가 소속된 채팅방 전체 중 가장 최신 채팅방으로 리디렉션
    try:
        latest_chat = ChatRoom.objects.filter(
            Q(receiver=user) | Q(starter=user)
        ).latest('latest_message_time')
        return redirect('carrot_app:chat_room', pk=latest_chat.room_number)

    # 3) 모두 없다면 현재 페이지로 리디렉션
    except ChatRoom.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'alert_message': '진행중인 채팅이 없습니다.',
            'redirect_url': 'main'
        })


# nav/footer에서 채팅하기 눌렀을 때
@login_required
def get_latest_chat_no_pk(request):
    user = request.user
    try:
        latest_chat = ChatRoom.objects.filter(
            Q(receiver=user) | Q(starter=user),
            latest_message_time__isnull=False
        ).latest('latest_message_time')
        return redirect('carrot_app:chat_room', pk=latest_chat.room_number)

    except ChatRoom.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'alert_message': 'There is no ChatRoom.',
            'redirect_url': 'main'
        })
        # return redirect('carrot_app:alert', alert_message='진행중인 채팅이 없습니다.', redirect_url='main')
    
@method_decorator(login_required, name='dispatch')
class ConfirmDealView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        previous_url = request.META.get('HTTP_REFERER')
        url_parts = previous_url.split('/')
        original_post_id = url_parts[-2] if url_parts[-1] == '' else url_parts[-1]

        chat_room = get_object_or_404(ChatRoom, room_number=original_post_id)


        if chat_room.starter == user:
            other_user = chat_room.receiver
        else:
            other_user = chat_room.starter

        if chat_room is None:
            messages.error(request, 'Chat room does not exist.')
            return redirect('carrot_app:trade')
        
        # buyer를 설정하고, status를 판매완료로 설정
        post.buyer = chat_room.receiver if chat_room.starter == post.user else chat_room.starter
        post.status = '판매완료'
        post.save()
        
        # 거래가 확정되면 새로고침
        return redirect('carrot_app:chat_room', pk=chat_room.room_number)