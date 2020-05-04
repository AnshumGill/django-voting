from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserAdminChangeForm,UserAdminCreationForm
# Register your models here.

User=get_user_model()

class UserAdmin(BaseUserAdmin):
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm
	search_fields=['phonenumber']
	list_display = ('phonenumber', 'fullname', 'admin','active')
	list_filter = ('admin','active')
	fieldsets = (
 		(None, {'fields': ('phonenumber', 'password')}),
		('Personal info', {'fields': ('fullname','address_line_1','address_line_2','city','state','pincode','user_hash')}),
		('Permissions', {'fields': ('admin','staff','active')}),
    )
    
	add_fieldsets = (
		(None, {
		    'classes': ('wide',),
		    'fields': ('phonenumber', 'password1', 'password2')}
		),
	)
	search_fields = ('phonenumber',)
	ordering = ('phonenumber',)
	filter_horizontal = ()

admin.site.register(User,UserAdmin)
