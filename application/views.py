from django.contrib import auth
from django.core import paginator
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.views.generic import View, ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Article, Comment, Tag
from .forms import UserCreateForm, CommentForm, SearchForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator

class IndexPageView(ListView):
    model = Article
    ordering = ["-published_date"]
    context_object_name = "articles"
    template_name = "application/index.html"
    paginate_by = 25

class IndexView(View):
    def get(self, request):
        articles = Article.objects.all().order_by("-published_date")
        #search_form = SearchForm()
        context = {
            "articles": articles,
            #"search_form": search_form,
        }

        return render(request, "application/index.html", context)


class SearchResultsView(View):
    def get(self, request):
        query_value = request.GET.get('q')
        print(f'Query Value: {query_value}')
        if query_value is not '':
            results = Article.objects.filter(tags__name__icontains=str(query_value)).distinct()
        else:
            results = None
        return render(request, "application/search-results.html", {
            "results": results
        })

class TagDetailView(View):
    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        related_articles = Article.objects.filter(tags__name__icontains=tag.name).distinct()

        context = {
            "related_articles": related_articles,
        }
        return render(request, "application/tag-detail.html", context)


class ArticleDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        comment_form = CommentForm()
        comments = article.comments.all().order_by("-id")

        context = {
            "article": article,
            "comment_form": comment_form,
            "comments": comments,
        }

        return render(request, "application/article-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        article = Article.objects.get(slug=slug)
        comments = article.comments.all().order_by("-id")
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.commentor = request.user
            comment.save()
            return HttpResponseRedirect(reverse("article-detail", args=[slug]))
        return render(
            request,
            "application/article-detail.html",
            {
                "article": article,
                "comment_form": comment_form,
                "comments": comments,
            },
        )


class MyLoginView(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            return super(MyLoginView, self).get(request, *args, **kwargs)


class SignupView(View):
    def get(self, request):
        print("Did a sign up view get")
        if request.user.is_authenticated:
            print("got into the auth block")
            return HttpResponseRedirect("/")
        form = UserCreateForm()
        return render(
            request,
            "register.html",
            {
                "form": form,
            },
        )

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("index")
        else:
            return render(
                request,
                "register.html",
                {
                    "form": form,
                },
            )

            
class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            comments = Comment.objects.filter(commentor=user)
            return render(request, "application/profile.html",
                {
                    "user": user,
                    "comments": comments,
                },
            )
        else:
            return HttpResponseRedirect("/")

class DeleteCommentView(View):
    def post(self, request, id):
        print("made it to the delete view")
        comment = Comment.objects.get(id=id)
        comment_article_slug = comment.article.slug
        comment.delete()
        return HttpResponseRedirect(reverse("article-detail", args=[comment_article_slug]))

class PersonalDeleteCommentView(View):
    def post(self, request, id):
        comment = Comment.objects.get(id=id)
        comment.delete()
        return HttpResponseRedirect(reverse("profile"))
