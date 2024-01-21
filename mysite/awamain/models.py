from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=255)
    book_cover = models.ImageField(null=True, blank=True, upload_to='images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    pub_date = models.DateField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField("Category", blank=True, related_name="posts")
    description = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name='book_post')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.title}  by {self.author}'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post.title} was commented by {self.body}'

