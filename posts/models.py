from django.db import models
from users.models import User
# from my_rooms.models import Book

# Create your models here.
class TimeStempedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True) 

    class Meta:
        abstract = True 

class Post(TimeStempedModel):

    RATING_CHOICES = (
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    )

    title = models.CharField(max_length=50)
    book_rating = models.IntegerField(choices=RATING_CHOICES, default=None)
    content = models.TextField()
    
    # book = models.ForeignKey(Book, related_name='posts', on_delete=models.SET_NULL)  # Null로 바뀐 다면 원래 Book을 참조하던 값들은 어떻게 되는 것인가..
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title