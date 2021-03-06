from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views.generic import ListView 
from .models import BookClub, ClubPost, Comment 
from users.models import User
from book_clubs.forms import CommentForm, ClubForm, ClubPostForm

# Create your views here.
class ClubListView(ListView):
    model = BookClub
    template_name = 'book_clubs/book_club_list.html'
    context_object_name = 'clubs' 
    paginate_by = 5
    ordering = ['-create_at']

def club_detail(request, club_id):
    if request.user.is_authenticated:
        # 해당 book_club에 속하는 포스트와 댓글을 모두 db에서 가져온다.
        club = get_object_or_404(BookClub, pk=club_id)
        user = get_object_or_404(User, pk=request.user.id) 
        club_posts = ClubPost.objects.filter(club=club)
        club_post_comment = Comment.objects.filter(club=club)

        # 해당 모임의 member이면 GET으로 member가 아니면 POST로 요청이 온다.
        if request.method == 'GET':
            comment_form = CommentForm() 

        elif request.method == 'POST':  # book_club에 참여하는 로직 
            # ManyToMany 관계에서 추가는 add() 삭제는 remove() 사용. db에 저장까지 된다.
            # book_club의 members 포함되어 있는 사람이 POST 요청을 보낼경우 모임을 탈퇴한다.
            if user in club.members.all():
                club.members.remove(request.user)
                return redirect('users:profile', user.id)
            
            else:
                club.members.add(request.user) 
                comment_form = CommentForm() 
        
        return render(
            request,
            'book_clubs/book_club_detail.html',
            {'club': club, 'club_posts': club_posts, 'comments': club_post_comment, 'comment_form': comment_form}
        )

    else:
        return render(request, 'book_clubs/login_required/login_required_enter.html')

def club_create(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)

        if request.method == 'GET':
            form = ClubForm(user=user) 

        elif request.method == 'POST':
            form = ClubForm(user, request.POST)
            if form.is_valid():
                new_club = form.save(commit=False)
                new_club.host = request.user 
                new_club.book.used_club = True 
                new_club.save() 
                new_club.book.save() 
                return redirect('clubs:club_list') 
            
        return render(request, 'book_clubs/create_book_club_form.html', {'form': form})
        
    else:
        return render(request, 'book_clubs/login_required/login_required_create.html')

def club_delete(request, club_id):
    if request.user.is_authenticated:
        club = get_object_or_404(BookClub, pk=club_id)
        if request.user != club.host:
            return redirect('clubs:club_detail', club_id=club.id)

        if request.method == 'GET':
            return render(request, 'book_clubs/club_confirm_delete.html', {'club': club})

        elif request.method == 'POST':
            club.book.used_club = False
            club.book.save() 
            club.delete()
            return redirect('clubs:club_list')
    else:
        return redirect('account_login')


def club_post_create(request, club_id):
    if request.user.is_authenticated:
        club = get_object_or_404(BookClub, pk=club_id)
        if request.method == 'GET':
            form = ClubPostForm() 
            return render(request, 'book_clubs/book_club_post_form.html', {'form': form, 'club': club})

        elif request.method == 'POST':
            form = ClubPostForm(request.POST)
            if form.is_valid():
                new_club_post = form.save(commit=False)
                new_club_post.author = request.user
                new_club_post.club = club 
                new_club_post.save() 
            return redirect('clubs:club_detail', club.id)
    else:
        return redirect('account_login') 

def club_post_update(request, club_id, post_id):
    if request.user.is_authenticated:
        club = get_object_or_404(BookClub, pk=club_id) 
        club_post = get_object_or_404(ClubPost, pk=post_id)

        if request.user != club_post.author:
            return redirect('account_login')

        if request.method == 'GET':
            form = ClubPostForm(instance=club_post)
            return render(request, 'book_clubs/book_club_post_form.html', {'form': form, 'clup_post': club_post, 'club': club})

        elif request.method == 'POST':
            form = ClubPostForm(request.POST) 
            if form.is_valid():
                club_post.title = form.cleaned_data['title']
                club_post.content = form.cleaned_data['content']
                club_post.save() 
                return redirect('clubs:club_detail', club_id=club_id) 
            return redirect('clubs:club_post_update', club_id=club_id, post_id=post_id)
    else:
        return redirect('account_login')

def club_post_delete(request, club_id, post_id):
    if request.user.is_authenticated:
        club_post = get_object_or_404(ClubPost, pk=post_id)
        # club = get_object_or_404(pk=club_id)
        if club_post.author != request.user:
            return redirect('clubs:club_detail', club_id=club_id)

        if request.method == 'GET':
            return render(request, 'book_clubs/club_post_confirm_delete.html', {'club_post': club_post})
        elif request.method == 'POST':
            club_post.delete() 
            return redirect('clubs:club_detail', club_id=club_id)
    else:
        return redirect('account_login')

def comment_create(request, club_id, post_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            club = get_object_or_404(BookClub, pk=club_id)
            post = get_object_or_404(ClubPost, pk=post_id)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False) 
                new_comment.club = club 
                new_comment.post = post 
                new_comment.author = request.user 
                new_comment.save() 
                return redirect(reverse('clubs:club_detail', kwargs={'club_id': club_id}) + '#comment-'+ str(new_comment.id))
                # return redirect('clubs:club_detail', club_id=club_id)
    else:
        return redirect('account_login')

def comment_delete(request, club_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.method == 'POST':
            comment.delete() 
        return redirect('clubs:club_detail', club_id=club_id )
    else:
        return redirect('account_login')

def club_out(reqeust, club_id):
    club = get_object_or_404(BookClub, pk=club_id)
    return render(reqeust, 'book_clubs/club_out_confirm.html', {'club': club}) 
