from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Account
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    # User Profile
    path('profile/', views.profile, name='profile'),
    path('<int:profile_id>/editprofile/', views.editprofile, name='editprofile'),
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('changepassword/', views.changepassword, name='changepassword'),
    # Posts and Comments
    path('posts/', views.posts, name='posts'),
    path('<int:post_id>/postpage/', views.postpage, name='postpage'),
    path('addphoto/', views.addphoto, name='addphoto'),
    path('editpost/<int:post_id>/', views.editpost, name='editpost'),
    path('deletepost/<int:post_id>/', views.deletepost, name='deletepost'),
    path('plike/<int:post_id>/', views.like_post, name='like_post'),
    path('<int:post_id>/postcomments/', views.postcomments, name='postcomments'),
    # Videos and Comments
    path('videos/', views.videos, name='videos'),
    path('<int:video_id>/videopage/', views.videopage, name='videopage'),
    path('addvideo/', views.addvideo, name='addvideo'),
    path('editvideo/<int:video_id>/', views.editvideo, name='editvideo'),
    path('deletevideo/<int:video_id>/', views.deletevideo, name='deletevideo'),
    path('vlike/<int:video_id>/', views.like_video, name='like_video'),
    path('<int:video_id>/videocomments', views.videocomments, name='videocomments'),
    # Chat Pages
    path('chatuser/', views.chatuser, name='chatuser'),
    path('<int:chatuser_id>/chatroom/', views.chatroom, name='chatroom'),
    path('groupchat/', views.groupchat, name='groupchat'),
    # Notifications
    path('notification/', views.notification, name='notification'),
    # About Section
    path('aboutteam/', views.aboutteam, name='aboutteam'),
    path('aboutme/', views.aboutme, name='aboutme'),
    path('description', views.description, name='description'),
    path('howtouse/', views.howtouse, name='howtouse'),
    path('faq/', views.faq, name='faq'),
    # Admin Settings
    path('adminpage/<int:user_id>/', views.adminpage, name='adminpage'),
    path('deleteuser/<int:user_id>/', views.deleteuser, name='deleteuser'),
    path('deletemember/<int:member_id>/', views.deletemember, name='deletemember'),
    path('deletecomment/<int:comment_id>/', views.deletecomment, name='deletecomment'),
    path('muteusr/<int:user_id>/', views.muteuser, name='muteuser'),
    path('addmember/', views.addmember, name='addmember'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
