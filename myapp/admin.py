from django.contrib import admin
from .models import *
admin.site.register(UserProfile)

admin.site.register(Telegram_Sub_Tasks)
admin.site.register(Category)

admin.site.register(Task)
admin.site.register(TaskUser)
admin.site.register(Task_Timer)
admin.site.register(TaskUser_Timer)



