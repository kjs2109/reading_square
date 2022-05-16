from django.urls import path 
from . import views 

app_name = 'clubs'
urlpatterns = [
    # book_clubs/
    path('', views.ClubListView.as_view(), name='club_list'),
    # book_clubs/1/detail/
    path('<int:club_id>/detail/', views.club_detail, name='club_detail'),
    # book_clubs/create/ 
    path('create/', views.club_create, name='club_create'),
    # book_clubs/1/delete/ 
    path('<int:club_id>/delete/', views.club_delete, name='club_delete'),
    # book_clubs/1/create_post/ 
    path('<int:club_id>/create_post/', views.club_post_create, name='club_post_create'),
    # book_clubs/1/update_post/1/ 

    # book_clubs/1/delete_post/1/

    # book_clubs/1/posts/1/create_comment/

    # book_clubs/1/delete_comment/ 
]