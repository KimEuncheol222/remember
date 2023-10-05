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
    is_liked_by_user = models.BooleanField(default=False)  # 좋아요 상태를 나타내는 필드 추가    

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

# 관심 상품
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wish_list')
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.title}'

# 사용자 프로필
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    region = models.ForeignKey(StandardArea, on_delete=models.SET_NULL, null=True)
    region_certification = models.CharField(max_length=1, default='N')
    certificated_at = models.DateTimeField(auto_now_add=True, null=True)
    rating_score = models.DecimalField(max_digits=3, decimal_places=1, default=36.5, null=True)
    wish_list = models.ManyToManyField(WishList, blank=True)

    def join_date(self):
        return self.user.date_joined

    def __str__(self):
        return f'{self.user.username} Profile'

# 채팅
class ChatRoom(models.Model):
    room_number = models.AutoField(primary_key=True)
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='started_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    latest_message_time = models.DateTimeField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='chat_rooms', null=True, blank=True)


    def __str__(self):
        return f'ChatRoom: {self.starter.username} and {self.receiver.username}'

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message: {self.author.username} at {self.timestamp}'

    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 새 메시지가 저장될 때마다 chatroom의 latest_message_time을 업데이트
        self.chatroom.latest_message_time = self.timestamp
        self.chatroom.save()