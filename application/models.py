from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, SET, SET_NULL
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import uuid

class Member(AbstractUser):
    email = models.EmailField(unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Member, on_delete=CASCADE, related_name="editorals")
    published_date = models.DateTimeField(auto_now_add=True, editable=False)
    snippet = models.CharField(max_length=250)
    text = RichTextField()
    slug = models.SlugField(unique=True, db_index=True, blank=True, max_length=255)
    tags = models.ManyToManyField(Tag, related_name="articles")
    image = models.URLField()
    top_post = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commentor = models.ForeignKey(
        Member, null=True, on_delete=SET_NULL, related_name="comments"
    )
    text = models.TextField(max_length=400)
    article = models.ForeignKey(
        Article, on_delete=SET_NULL, null=True, related_name="comments"
    )

    def __str__(self):
        return f"Comment by {self.commentor} on Article: {self.article}"
