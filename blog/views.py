# from unicodedata import category
from urllib import request
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Create your views here.

from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from .forms import PostForm, EditForm

class HomeView(ListView):
    model = Post
    template_name = "blog/home.html"
    cats = Category.objects.all()
    ordering = [ '-post_date' ]

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'blog/category_list.html', {'cat_menu_list': cat_menu_list })

def searched_post(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        #searched = request.POST['searched']
        return render(request, 'blog/searched_post.html', {'searched':searched})
    else:
        return render(request, 'blog/searched_post.html', {})



def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'blog/categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts})


class ArticleDetailView(DetailView):
    model = Post
    template_name = "blog/article_details.html"


    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class AddCategoryView(CreateView):
    model = Category
    template_name = "blog/add_category.html"
    fields = ('name',)
    # fields = '__all__'
    # form_class = PostForm

def addpost(request):
    submitted = False
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('addpost?submitted=True')
    else:
        form = PostForm
        if "submitted" in request.GET:
            submitted = True
        return render(request, "blog/add_post.html", {'form':form, 'submitted':submitted})


class UpdatePostView(UpdateView):
    model = Post
    template_name = "blog/update_post.html"
    form_class = EditForm
    # fields = ["name", "title_tag", "body"]
    # fields = "__all__"


class DeletePostView(DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy('home')