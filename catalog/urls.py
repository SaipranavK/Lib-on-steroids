from django.urls import path
from . import views

app_name="catalog"

urlpatterns = [
    path('push/',views.book_create,name="book-create"),
    path('search/',views.book_search,name="book-search"),
    path('search-page/',views.book_searchpage,name="book-search-page"),
    path('trans-search/',views.book_trans_search,name="book-trans-search"),
    path('mtrans-search/',views.book_mtrans_search,name="book-mtrans-search"),
    path('edit/<int:booknumber>/',views.book_edit,name="book-edit"),
    path('delete/<int:booknumber>/',views.book_delete,name="book-delete"),
    path('delete/confirm/<int:booknumber>/',views.book_delete_confirm,name="book-delete-confirm"),
]