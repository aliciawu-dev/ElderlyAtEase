from django.contrib import admin
from .models import Profile, Connect, VerifyInfo

admin.site.register(Profile)
admin.site.register(Connect)
admin.site.register(VerifyInfo)