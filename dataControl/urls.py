from django.urls import path
from . import views

app_name="dataControl"

urlpatterns=[
	path('bulk-import/',views.BulkImport, name="bulk-import"),
	path('exports/',views.DataExports, name="exports"),
]