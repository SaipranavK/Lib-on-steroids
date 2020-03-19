from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Profile,User

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','gender','branch','phone','barcode','pin')

class UserAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_class = UserResource

admin.site.register(User, UserAdmin)
admin.site.register(Profile)

BaseAdmin.fieldsets += ('Custom fields set', {'fields': ['gender','branch','phone','barcode','pin']}),