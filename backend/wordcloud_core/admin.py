from django.contrib import admin
from .models import UserProfile, WordCloud, UserCredit

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mfa_enabled', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('mfa_enabled',)

@admin.register(WordCloud)
class WordCloudAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username', 'user__email')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserCredit)
class UserCreditAdmin(admin.ModelAdmin):
    list_display = ('user', 'credits_remaining', 'last_updated')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('last_updated',)
