from django.contrib import admin

from.models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Member)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(Video)
admin.site.register(VideoLike)
admin.site.register(VideoComment)
admin.site.register(Messages)
admin.site.register(Notification)
admin.site.register(GroupChat)

