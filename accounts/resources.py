from import_export import resources
from .models import User

class StudentResource(resources.ModelResource):
	class Meta:
		model=User
