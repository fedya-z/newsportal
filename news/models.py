from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    rating_author = models.FloatField(default=0.0)


    def update_rating(self):
        posts_rating = self.post_set.aggregate(total=models.Sum('rating_post'))['total'] or 0
        posts_rating *= 3

        comments_rating = self.user.comment_set.aggregate(total=models.Sum('rating_comment'))['total'] or 0

        comments_on_posts_rating = Comment.objects.filter(post__author=self).aggregate(
            total=models.Sum('rating_comment')
        )['total'] or 0

        self.rating_author = posts_rating + comments_rating + comments_on_posts_rating
        self.save()

    def __str__(self):
        return self.author_name.title()

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique = True)

    def __str__(self):
        return self.category_name.title()


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    post_name = models.CharField(max_length=255)
    text_post = models.CharField(max_length=255)
    rating_post = models.FloatField(default=0.0)
    time_in_post = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField( max_length=2,choices=POST_TYPE_CHOICES,default=ARTICLE,)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text_post[:124] + '...' if len(self.text_post) > 124 else self.text_post

    def __str__(self):
        return f'{self.post_name.title()}: {self.description[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)



class Comment(models.Model):
    comment_text = models.CharField(max_length=255)
    time_in_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.FloatField(default=0.0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_text.title()}: {self.description[:20]}'