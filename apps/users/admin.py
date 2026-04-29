from django.contrib import admin

from django.contrib.auth import get_user_model
from .models import DeviceLock
from .forms import MessageAdminForm

User = get_user_model()


admin.site.site_header = "My Company Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to the Dashboard"


# @admin.register(User)
# class CustomAdmin(admin.ModelAdmin):
#     form = MessageAdminForm
#     list_display = ('id','username','name')
#     list_display_links = ['id','username','name']
#     list_per_page = 2
#     search_fields = ('username',)
#     list_filter = ('created_at',)
#     readonly_fields = ['created_at']
#     empty_value_display = "-empty-"

admin.site.register(User)
admin.site.register(DeviceLock)
