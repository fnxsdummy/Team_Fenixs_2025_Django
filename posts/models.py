from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  p_image = models.ImageField(upload_to='media/', null=True, blank=True, default='images/profile.jpg')
  p_bio = models.TextField(null=True, blank=True, default='Add your Bio')
  p_gender = models.TextField(null=True, blank=True, default='Add your Gender')
  p_birthday = models.DateField(null=True, blank=True, default='2000-01-01')
  p_phone = models.TextField(null=True, blank=True, default='Add your Number')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f'{self.user.username} || Profile'
  


class Member(models.Model):
  m_image = models.ImageField(upload_to='media/')
  m_name = models.CharField(max_length=100)
  m_role = models.CharField(max_length=100)
  m_description = models.TextField()
  m_insta = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f'{self.m_name} || {self.m_role}'
  


class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  user_image = models.ImageField(upload_to='media/', null=True, blank=True)
  img = models.ImageField(upload_to='media/')
  title = models.CharField(max_length=100, blank=True, null=True)
  description = models.TextField(null=True, blank=True)
  location = models.CharField(max_length= 200, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def total_likes(self):
    return self.plikes.count()
  
  def __str__(self):
    return f'{self.user.username} || {self.title}'
  

class PostLike(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post,related_name='plikes' ,on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f'{self.user.username} || {self.post.title}'

class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name="pcomments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.post.title}'

# Post Videos
class Video(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  user_image = models.ImageField(upload_to='media/', null=True, blank=True)
  video = models.FileField(upload_to='media/')
  title = models.CharField(max_length=100, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  location = models.CharField(max_length= 200, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def total_likes(self):
    return self.vlikes.count()
  
  def __str__(self):
    return f'{self.user.username} || {self.title}'
  

class VideoLike(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  video = models.ForeignKey(Video, related_name='vlikes', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f'{self.user.username} || {self.video.title}'
  

class VideoComment(models.Model):
    video = models.ForeignKey(Video, related_name="vcomments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.video.title}'

  
class Messages(models.Model):
  sender = models.ForeignKey(User, related_name='s_messages', on_delete=models.CASCADE)
  receiver = models.ForeignKey(User, related_name='r_messages', on_delete=models.CASCADE)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f'{self.sender.username} to {self.receiver.username}'
  
  
class Notification(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, blank=True, null=True)
  id_number = models.IntegerField()
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  def __str__(self):
    return f'{self.user.username} || {self.content}'
  
class GroupChat(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.TextField()
  is_sender = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  def __str__(self):
    return f'{self.user.username} || {self.text}'

  
  
  
  
  
  
  