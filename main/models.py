from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.db import models

 
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    onesignal_player_id = models.CharField(max_length=200, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    def __str__(self):
        return self.phone if self.phone else self.username

class UserFollow(models.Model):
    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following'
    )  # 👉 follower = OBUNA BO‘LGAN odam (men)

    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers'
    ) # 👉 following = OBUNA BO‘LINAYOTGAN odam (unga obuna bo‘ldim)


    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower_id} -> {self.following_id}"

    # user.followers.all() → unga obuna bo‘lganlar

    # user.following.all() → u obuna bo‘lganlar

class Banner(models.Model):
    image = models.ImageField(upload_to="banners/")

    def __str__(self):
        return f"Banner {self.id}"


class ChatRoom(models.Model):
    product = models.ForeignKey(
        'announcement.Product', on_delete=models.CASCADE, related_name="chat_rooms"
    ,null=True, blank=True)
    user_1 = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_user1"
    )
    user_2 = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_user2"
    )
    owner = models.ForeignKey( 
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_chats"
    )
    
    room_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_1", "user_2", ], name="unique_chat_between_users"
            )
        ]

    def save(self, *args, **kwargs):
        # user_1 va user_2 tartibini kafolatlash (masalan, doim kichik id birinchi)
        if self.user_1.id > self.user_2.id:
            self.user_1, self.user_2 = self.user_2, self.user_1
        ids = sorted([self.user_1.id, self.user_2.id])
        self.room_name = f"chat_{ids[0]}_{ids[1]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Chat between {self.user_1} and {self.user_2}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    flowed = models.BooleanField(default=False)
    def __str__(self):
        return f"Message from {self.sender} in {self.room}"


class FCMToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'token')
    
    def __str__(self):
        return f"FCM Token for {self.user}"

