from django.contrib import admin
from .models import Article, Tag, Comment, Member


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_date"]


admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Member)