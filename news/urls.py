from django.urls import path
from .views import PostsList, PostDetail, SearchPage, PostCreate, PostUpdate, PostDelete, ArticleCreate, ArticleUpdate, ArticleDelete, subscriptions
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', cache_page(300)(SearchPage.as_view()), name='search'),
    path('create/', cache_page(300)(PostCreate.as_view()), name='post_create'),
    path('<int:pk>/edit/', cache_page(300)(PostUpdate.as_view()), name='post_edit'),
    path('<int:pk>/delete/', cache_page(300)(PostDelete.as_view()), name='post_delete'),
    path('articles/create/', cache_page(300)(ArticleCreate.as_view()), name='article_create'),
    path('articles/<int:pk>/edit/', cache_page(300)(ArticleUpdate.as_view()), name='article_edit'),
    path('articles/<int:pk>/delete/', cache_page(300)(ArticleDelete.as_view()), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]