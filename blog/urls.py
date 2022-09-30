from django.urls import path

from . import views

from .views import HomeView,ArticleDetailView,AddCategoryView,UpdatePostView, DeletePostView,  CategoryView, CategoryListView, searched_post, addpost, LikeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('addpost', views.addpost, name='addpost'),
    path('addpost', addpost, name='addpost'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('category_list/', CategoryListView, name='category-list'),
    path('add_category/', AddCategoryView.as_view(), name='add-category'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-details'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='update-post'),
    path('<int:pk>/remove', DeletePostView.as_view(), name='delete-post'),
    path('search_post/', searched_post, name='searched-post'),
    path('like/<int:pk>', LikeView, name='like_post'),
]



