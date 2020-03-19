from import_export import resources
from .models import Transaction

class TransactionResource(resources.ModelResource):
	class Meta:
		model=Transaction
