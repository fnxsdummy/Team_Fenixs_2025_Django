from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Post, Member, Profile, Video, PostLike, VideoLike, PostComment, VideoComment, Messages, Notification, GroupChat
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# HOME VIEW
def home(request):
    posts = Post.objects.select_related('user__profile').all().order_by('-created_at')[0:5]
    members = Member.objects.all()
    liked_posts = PostLike.objects.filter(user=request.user).values_list('post_id', flat=True) if request.user.is_authenticated else []
    liked_videos = VideoLike.objects.filter(user=request.user).values_list('video_id', flat=True) if request.user.is_authenticated else []
    return render(request, 'home.html', {'posts': posts, 'members': members, 'liked_posts': liked_posts, 'liked_videos': liked_videos})

# PROFILE VIEW
@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    videos = Video.objects.filter(user=user).order_by('-created_at')
    profile = Profile.objects.get_or_create(user=user)
    info = Profile.objects.get(user=user)
    liked_posts = PostLike.objects.filter(user=request.user).values_list('post_id', flat=True) if request.user.is_authenticated else []
    liked_videos = VideoLike.objects.filter(user=request.user).values_list('video_id', flat=True) if request.user.is_authenticated else []
    postscount = posts.count()
    videoscount = videos.count()
    total = postscount + videoscount
    return render(request, 'profile.html', {'user': user, 'posts': posts, 'profile': profile, 'info': info, 'videos': videos, 'total': total, 'liked_posts': liked_posts, 'liked_videos': liked_videos})

# EDIT PROFILE INFORMATION
@login_required
def editprofile(request, profile_id):
    user = request.user
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        image = request.FILES.get('profilePhoto')
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        phone = request.POST['phoneNumber']
        birthday = request.POST['dob']
        gender = request.POST['gender']
        bio = request.POST['bio']
        profile.p_phone = phone
        profile.p_birthday = birthday
        profile.p_gender = gender
        if bio:
            profile.p_bio = bio
        if image:
            profile.p_image = image
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile.save()
        return redirect('profile')
    return render(request, 'editprofile.html', {'user': user, 'profile': profile})

# AUTHENTICATION AND ACCOUNT ACCESS
# ================================================================

# LOGIN VIEW
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login
            return redirect('profile')
        else:
            return redirect('login')
    return render(request, 'registration/login.html')

# LOGOUT VIEW
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')

# SIGNUP VIEW
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phonenumber']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile = Profile.objects.create(user=user, p_phone=phone, p_birthday=birthday, p_gender=gender)
        Notification.objects.create(user=user, name=user.username, id_number=user.id, content='joined our app')
        return redirect('home')
    return render(request, 'signup.html')

# CHANGE PASSWORD VIEW
@login_required
def changepassword(request):
    user = request.user
    if request.method == 'POST':
        current_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')
        user = authenticate(username=request.user.username, password=current_password)
        
        if user is not None:
            # Validate new password and confirm password
            if new_password == confirm_password:
                # Change password
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('home')
            else:
                messages.error(request, 'New password and confirm password do not match.')
        else:
            messages.error(request, 'The current password is incorrect.')
    return render(request, 'changepassword.html')

# POSTS
# =============================================================

# POSTS PAGE VIEWS
@login_required
def posts(request):
    posts = Post.objects.all().order_by('-created_at')
    liked_posts = PostLike.objects.filter(user=request.user).values_list('post_id', flat=True) if request.user.is_authenticated else []
    liked_videos = VideoLike.objects.filter(user=request.user).values_list('video_id', flat=True) if request.user.is_authenticated else []
    return render(request, 'posts.html', {'posts': posts, 'liked_posts': liked_posts, 'liked_videos': liked_videos})

# SINGLE POST PAGE VIEW
@login_required
def postpage(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    liked_posts = PostLike.objects.filter(user=request.user).values_list('post_id', flat=True) if request.user.is_authenticated else []
    pcomments = post.pcomments.all()
    return render(request, 'postpage.html', {'user': user, 'post': post, 'liked_posts': liked_posts, 'pcomments': pcomments})

# ADD PHOTOS
@login_required
def addphoto(request):
    if request.method == 'POST':
        user = request.user
        img = request.FILES.get('photo')
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        user_image = Profile.objects.get(user=user).p_image
        post = Post.objects.create(user=user, user_image=user_image, img=img, title=title, description=description, location=location)
        Notification.objects.create(user=user, name=user.username, id_number=post.id, content='posted a photo')
        return redirect('posts')
    return render(request, 'addphoto.html')

# EDIT PHOTOS

def editpost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        img = request.FILES.get('photo')
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        if img:
            post.img = img
        if title:
            post.title = title
        if description:
            post.description = description
        if location:
            post.location = location
        post.save()
        return redirect('postpage', post_id=post.id)
    return render(request, 'editpost.html', {'post': post})

# DELETE PHOTOS

def deletepost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('posts')

# LIKE PHOTOS
@login_required
def like_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    plike, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        plike.delete()
    Notification.objects.create(user=request.user, name=request.user.username, id_number=post.id, content='liked a post')
    if user.is_authenticated:
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)
    return redirect('home')

# COMMENT PHOTOS
@login_required
def postcomments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.pcomments.all()
    referer = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            PostComment.objects.create(post=post, user=request.user, content=content)
            Notification.objects.create(user=request.user, name=request, id_number=post.id, content='commented on a post')
            return redirect(referer, post_id=post.id)
    return render(request, referer, {'post': post, 'comments': comments})


# VIDEOS
# =============================================================

# VIDEOS PAGE VIEWS
@login_required
def videos(request):
    videos = Video.objects.all().order_by('-created_at')
    liked_videos = VideoLike.objects.filter(user=request.user).values_list('video_id', flat=True) if request.user.is_authenticated else []
    return render(request, 'videos.html', {'videos': videos, 'liked_videos': liked_videos})

# SINGLE VIDEO PAGE VIEW
@login_required
def videopage(request, video_id):
    user = request.user
    video = get_object_or_404(Video, id=video_id)
    liked_videos = VideoLike.objects.filter(user=request.user).values_list('video_id', flat=True) if request.user.is_authenticated else []
    vcomments = video.vcomments.all()
    return render(request, 'videopage.html', {'user': user, 'video': video, 'liked_videos': liked_videos, 'vcomments': vcomments})

# ADD VIDEOS
@login_required
def addvideo(request):
    if request.method == 'POST':
        user = request.user
        video = request.FILES.get('photo')
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        user_image = Profile.objects.get(user=user).p_image
        video = Video.objects.create(user=user, user_image=user_image, video=video, title=title, description=description, location=location)
        Notification.objects.create(user=user, name=user.username, id_number=video.id, content='upload a video')
        return redirect('videos')
    return render(request, 'addvideo.html')

# EDIT VIDEO

def editvideo(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        new_video = request.FILES.get('photo')
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        if video:
            video.video = new_video
        if title:
            video.title = title
        if description:
            video.description = description
        if location:
            video.location = location
        video.save()
        return redirect('videopage', video_id=video.id)
    return render(request, 'editvideo.html', {'video': video})

# DELETE VIDEO

def deletevideo(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.delete()
    return redirect('videos')


# LIKE VIDEOS
@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    vlike, created = VideoLike.objects.get_or_create(video=video, user=request.user)
    if not created:
        vlike.delete()
    referer = request.META.get('HTTP_REFERER', '/')
    Notification.objects.create(user=request.user, name=request.user.username, id_number=video.id, content='liked a video')
    return redirect(referer)

# COMMENT VIDEOS
@login_required
def videocomments(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    vcomments = video.vcomments.all()
    referer = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            VideoComment.objects.create(video=video, user=request.user, content=content)
            Notification.objects.create(user=request.user, name=request.user.username, id_number=video.id, content='commented on a video')
            return redirect(referer, video_id=video.id)
    return render(request, referer, {'video': video, 'vcomments': vcomments})


# CHAT WITH USERS AND CHAT ROOMS
# ==================================================================

# USER LISTS
@login_required
def chatuser(request):
    user = request.user
    users = User.objects.all()
    return render(request, 'chatusers.html', {'user': user, 'users': users})

# CHAT ROOM AND MESSAGES
@login_required
def chatroom(request, chatuser_id):
    user_1 = request.user
    user_2 = User.objects.get(id=chatuser_id)
    all_messages_1 = Messages.objects.filter(sender=user_1, receiver=user_2)
    all_messages_2 = Messages.objects.filter(sender=user_2, receiver=user_1)
    all_messages = all_messages_1.union(all_messages_2)
    if request.method == 'POST':
        message_content = request.POST['messageInput']
        Messages.objects.create(sender=user_1, receiver=user_2, content=message_content)
        return redirect('chatroom', chatuser_id=chatuser_id)
    return render(request, 'chatroom.html', {'all_messages': all_messages, 'user_1': user_1, 'user_2': user_2})

# GROUP CHAT 
@login_required
def groupchat(request):
    user = request.user
    messages = GroupChat.objects.all()
    if request.method == 'POST':
        message_content = request.POST['messageInput']
        GroupChat.objects.create(user=user, text=message_content)
        return redirect('groupchat')
    return render(request, 'groupchat.html', {'user': user, 'messages': messages})

# NOTIFICATIONS VIEW
@login_required
def notification(request):
    user = request.user
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})


# ABOUT SECTION AND DESCRIPTION
# ========================================================

# ABOUT TEAM
def aboutteam(request):
    return render(request, 'aboutteam.html')

# ABOUT ME
def aboutme(request):
    return render(request, 'aboutme.html')

# DESCRIPTION
def description(request):
    return render(request, 'description.html')

# HOW TO USE
def howtouse(request):
    return render(request, 'howtouse.html')

# FAQ

def faq(request):
    return render(request, 'faq.html')

# ADMIN PAGE    
@login_required
def adminpage(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        users = User.objects.all()
        members = Member.objects.all()
        posts = Post.objects.filter(user=user)
        videos = Video.objects.filter(user=user)
        postcomments = PostComment.objects.filter(user=user)
        videocomments = VideoComment.objects.filter(user=user)
        all_comments = postcomments.union(videocomments)
        groupmessages = GroupChat.objects.filter(user=user)
        return render(request, 'adminpage.html', {'users': users, 'posts': posts, 'videos': videos, 'all_comments': all_comments, 'groupmessages': groupmessages, 'members': members})       
    user = get_object_or_404(User, id=user_id)
    users = User.objects.all()
    members = Member.objects.all()
    posts = Post.objects.filter(user=user)
    videos = Video.objects.filter(user=user)
    postcomments = PostComment.objects.filter(user=user)
    videocomments = VideoComment.objects.filter(user=user)
    all_comments = postcomments.union(videocomments)
    groupmessages = GroupChat.objects.filter(user=user)
    return render(request, 'adminpage.html', {'users': users, 'posts': posts, 'videos': videos, 'all_comments': all_comments, 'groupmessages': groupmessages, 'members': members})
    

@login_required
def deleteuser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        return redirect('home')
    else:
        user.delete()
    return redirect('home')

@login_required
def muteuser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_active == True:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('home')

@login_required
def deletemember(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('home')

@login_required
def deletecomment(request, comment_id):
    comment = get_object_or_404(PostComment, id=comment_id)
    comment.delete()
    return redirect('home')
@login_required
def deletemessage(request, message_id):
    message = get_object_or_404(GroupChat, id=message_id)
    message.delete()
    return redirect('home')

@login_required
def addmember(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST['name']
        role = request.POST['role']
        description = request.POST['description']
        instagram = request.POST['instagram']
        member = Member.objects.create(m_image=image, m_name=name, m_role=role, m_description=description, m_insta=instagram)
        member.save()
        return redirect('home')
    return render(request, 'addmember.html')
    



