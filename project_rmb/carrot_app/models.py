from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


# Create your models here.

# 게시글 작성
class Post(models.Model):

    STATUS_CHOICES = (
    ('판매중', '판매중'),
    ('예약중', '예약중'),
    ('판매완료', '판매완료'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, to_field='username')
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='판매중')
    description = models.TextField()
    images = models.ImageField(upload_to='post_images/', null=True) 
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) 
    refreshed_at = models.DateTimeField(default=timezone.now) 
    view_num = models.PositiveIntegerField(default=0)  
    chat_num = models.PositiveIntegerField(default=0)
    wish_num = models.PositiveIntegerField(default=0)    

    def update_chat_count(self):
        # 해당 포스트와 연관된 채팅방 개수 계산
        chat_count = ChatRoom.objects.filter(product_id=self).count()
        self.chat_num = chat_count
        self.save()

    def update_wish_count(self):
        # 해당 포스트와 연관된 관심 수 계산
        wish_count = WishList.objects.filter(product_id=self).count()
        self.wish_num = wish_count
        self.save()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


# 행정 지역
class StandardArea(models.Model):
    area_name = models.CharField(max_length=100)
    city_id = models.IntegerField(null=True)
    city_name = models.CharField(max_length=100)
    version = models.DateTimeField(auto_now_add=True)


# 사용자 프로필
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    region = models.ForeignKey(StandardArea, on_delete=models.SET_NULL, null=True)
    region_certification = models.CharField(max_length=1, default='N')
    certificated_at = models.DateTimeField(auto_now_add=True, null=True)
    rating_score = models.DecimalField(max_digits=3, decimal_places=1, default=36.5, null=True)

    def join_date(self):
        return self.user.date_joined

    def __str__(self):
        return f'{self.user.username} Profile'


# 채팅 방
class ChatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_chat_room')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_chat_room', default=2)
    created_at = models.DateTimeField(auto_now_add=True)

    # 해당 채팅 방 user의 모든 상품 리스트 가져오기
    def get_user_products(self):
        return Post.objects.filter(user=self.user)

    def __str__(self):
        return f'ChatRoom ID: {self.user.id} with {self.buyer.id}'


# 채팅 메시지
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # 현재 로그인한 사용자 가져오기
        current_user = self.sender

        # 다른 사용자 가져오기 (chat_room의 buyer)
        other_user = self.chat_room.buyer

        # 현재 로그인한 사용자와 다른 사용자가 같지 않은 경우 buyer 필드 설정
        if current_user != other_user:
            self.sender = other_user

        super().save(*args, **kwargs)


# 관심 상품
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wish_list')
    product_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)