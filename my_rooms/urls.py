from django.urls import path 
from . import views 

app_name = 'my_rooms'
urlpatterns = [
    # my_room/1/books/
    path('<int:user_id>/books/', views.books, name='books'),
    # my_room/1/book_status/1/
    path('<int:user_id>/book_status/<int:book_id>/', views.edit_book_status, name='edit_book_status'),
    # my_room/1/add_book/ 
    
    # my_room/1/edit_book/1/

    # my_room/1/delete_book/1/
]