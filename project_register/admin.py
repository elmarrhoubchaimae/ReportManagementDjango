# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('user_type', 'school_year', 'field', 'department')  # Specify fields to display

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = UserAdmin.list_display + ('get_user_type', 'get_school_year', 'get_field', 'get_department')

    def get_user_type(self, obj):
        return obj.profile.user_type
    get_user_type.short_description = 'User Type'

    def get_school_year(self, obj):
        return obj.profile.school_year
    get_school_year.short_description = 'School Year'

    def get_field(self, obj):
        return obj.profile.field
    get_field.short_description = 'Field'

    def get_department(self, obj):
        return obj.profile.department
    get_department.short_description = 'Department'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
