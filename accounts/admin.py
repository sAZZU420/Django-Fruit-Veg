from django.contrib import admin
from .models import Account, UserProfile
from django.utils.html import format_html


class AccountAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "is_superuser", "is_admin", "is_staff", "is_active", "date_joined", "last_login")
    list_filter = ("email", "username", "is_staff", "is_active",)
    list_display_links = ('email', 'username',)
    search_fields = ("email",)
    ordering = ("-date_joined",)


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, objects):
        return format_html("<img src='{}' width='30' style='border-radius:50%;'>".format(objects.profile_pic.url))
    thumbnail.short_description = "profile pic"
    list_display = ("thumbnail", "user", "address_line_1", "city", "country", "date_joined",)
    list_filter = ("user", "date_joined",)
    list_display_links = ('user',)
    search_fields = ("user",)
    ordering = ("-date_joined",)


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
