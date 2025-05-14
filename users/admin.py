from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_call_count', 'api_call_limit')
    search_fields = ('user__username', 'user__email')
