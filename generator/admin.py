from django.contrib import admin
from .models import GenerationRequest

# Register your models here.
@admin.register(GenerationRequest)
class GenerationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game', 'status', 'created_at', 'completed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'game__title', 'prompt')
    readonly_fields = ('created_at', 'completed_at')
