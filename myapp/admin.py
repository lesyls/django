from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ContactRequest, UserProfile
from .models import Review


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service', 'status', 'created_at')
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'phone', 'email', 'service', 'message')
        }),
        ('Статус заявки', {
            'fields': ('status', 'admin_notes', 'created_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            # Здесь можно добавить отправку уведомления при изменении статуса
            pass
        super().save_model(request, obj, form, change)

# Перерегистрируем UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'status', 'created_at', 'short_text')
    list_filter = ('status', 'rating', 'created_at')
    list_editable = ('status',)
    search_fields = ('user__username', 'text')
    readonly_fields = ('created_at',)

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    short_text.short_description = 'Текст отзыва'

    fieldsets = (
        ('Информация об отзыве', {
            'fields': ('user', 'rating', 'text', 'created_at')
        }),
        ('Модерация', {
            'fields': ('status', 'admin_notes')
        }),
    )