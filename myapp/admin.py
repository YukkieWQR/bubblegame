from django.contrib import admin
from .models import *
admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Mining)
admin.site.register(MiningCard)
admin.site.register(Category)



