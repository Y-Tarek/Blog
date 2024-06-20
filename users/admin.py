from django.contrib import admin
from .models import User, Profile
from django.utils.html import format_html

class ProfileAdmin(admin.ModelAdmin):
    @admin.display(description="user")
    def get_user(self):
        try:
            return self.user.email
        except:
            return None
        
    @admin.display(description="image")
    def display_image(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="100" height="100" />', obj.profile_picture.url)
        else:
            return 'No image'
        
    list_per_page=10
    list_display = ["id","display_image",get_user]
admin.site.register(User)
admin.site.register(Profile,ProfileAdmin)
