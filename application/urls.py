from django.urls import path
from . import views
urlpatterns = [
    path("", views.IndexPageView.as_view(), name="index"),
    path("<slug:slug>", views.ArticleDetailView.as_view(), name="article-detail"),
    path("search/", views.SearchResultsView.as_view(), name="search-results"),
    path("tag/<slug:slug>", views.TagDetailView.as_view(), name="tag-detail"),
    path("delete/<uuid:id>", views.DeleteCommentView.as_view(), name="delete-comment"),
    path("comment/delete/<uuid:id>", views.PersonalDeleteCommentView.as_view(), name="profile-comment-delete"),
]
