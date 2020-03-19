from django.urls import path
from . import views

app_name="transactions"

urlpatterns = [
    path('manager/',views.transaction_manager,name="transaction-manager"),
    path('manager/kiosk/',views.transaction_manager_kiosk,name="transaction-manager-kiosk"),
    path('ajax/trans-stack/',views.transaction_stack,name="transaction-stack"),
    path('ajax/trans-stack-kiosk/',views.transaction_stack_kiosk,name="transaction-stack-kiosk"),
    path('ajax/admin-trans-search/',views.admin_trans_search,name="admin-trans-search"),
    path('ajax/admin-user-search/',views.admin_user_search,name="admin-user-search"),
    path('addStack/',views.transactionStackAdd,name="transaction-stack-add"),
    path('delStack/',views.transactionStackDelete,name="transaction-stack-delete"),
    path('transaction-filters/',views.transactionFilters,name="transaction-filters"),
    path('charts/gender/',views.chartsView,name="transactions-gender-chart"),
]