from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Transaction

class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ('user','book','issue_date')

class TransactionAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource

admin.site.register(Transaction, TransactionAdmin)

