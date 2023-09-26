from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


# Create your models here.
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
    refreshed_at = models.DateTimeField() 
    view_num = models.PositiveIntegerField(default=0)  
    chat_num = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    is_staff = models.BooleanField(default=False)
    region = models.CharField(max_length=100, null=True)
    region_certification = models.CharField(max_length=1, default='N')
    join_date = models.DateTimeField(auto_now_add=True)
    rating_score = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f'{self.user.username} Profile'
    

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)