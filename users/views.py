from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from posts.models import Post 
from users.models import User
from my_rooms.models import Book


# Create your views here.
def profile(request, user_id):
    if request.user.is_authenticated:
        profile_user = get_object_or_404(User, pk=user_id)
        user_posts = Post.objects.filter(author__id=user_id).order_by('-create_at')[:3]
        count_readed_book = Book.objects.filter(Q(user=profile_user) & Q(status=3)).count()
        return render(request, 'users/profile.html', {'profile_user': profile_user, 'user_posts': user_posts, 'count_readed_book': count_readed_book})
    else:
        return render(request, 'users/login_required.html')

def post_list(request, user_id):
    if request.user.is_authenticated:
        profile_user = get_object_or_404(User, pk=user_id)
        user_post_list = Post.objects.filter(author=profile_user)
        paginator = Paginator(user_post_list, 9)
        curr_page_number = request.GET.get('page')
        if curr_page_number is None:
            curr_page_number = 1 
        page = paginator.page(curr_page_number)
        return render(request, 'users/user_post_list.html', {'profile_user': profile_user, 'page': page})

    else:
        return render(request, 'users/login_required.html')