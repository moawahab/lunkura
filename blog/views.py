from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

# Create your views here.

from django.views import generic
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("article-details", args=[str(pk)]))


    # looking up a post whatever the post id was that was clicked
    # so post_id is the id giving to our clickacle button or replace with whatever the clickable button id was
    # we pass in the request and it contains the user id if they're log in

class HomeView(ListView):
    model = Post
    template_name = "blog/home.html"
    cats = Category.objects.all()
    ordering = ["-post_date"]

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, "blog/category_list.html", {"cat_menu_list": cat_menu_list})


def searched_post(request):
    if request.method == "POST":
        searched = request.POST.get("searched", False)
        # searched = request.POST['searched']
        return render(request, "blog/searched_post.html", {"searched": searched})
    else:
        return render(request, "blog/searched_post.html", {})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace("-", " "))
    return render(
        request,
        "blog/categories.html",
        {"cats": cats.title().replace("-", " "), "category_posts": category_posts},
    )


class ArticleDetailView(DetailView):
    model = Post
    template_name = "blog/article_details.html"

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

        stuff = get_object_or_404(Post, id=self.kwargs["pk"])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


        # if stuff.likes.filter(id=self.request.id).exists():
        #     liked = True






class AddCategoryView(CreateView):
    model = Category
    template_name = "blog/add_category.html"
    fields = ("name",)
    # fields = '__all__'
    # form_class = PostForm


def addpost(request):
    submitted = False
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("addpost?submitted=True")
    else:
        form = PostForm
        if "submitted" in request.GET:
            submitted = True
        return render(
            request, "blog/add_post.html", {"form": form, "submitted": submitted}
        )


class AddCommentView(CreateView):
    model = Comment
    template_name = "blog/add_comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    template_name = "blog/update_post.html"
    form_class = EditForm
    # fields = ["name", "title_tag", "body"]
    # fields = "__all__"


class DeletePostView(DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy("home")
