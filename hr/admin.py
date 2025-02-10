from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, HRProfile

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_hr', 'is_candidate', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_hr', 'is_candidate', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    list_filter = ('is_hr', 'is_candidate', 'is_staff')

class HRProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position')
    search_fields = ('user__email', 'company')
    list_filter = ('company',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(is_hr=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(User, CustomUserAdmin)
admin.site.register(HRProfile, HRProfileAdmin)