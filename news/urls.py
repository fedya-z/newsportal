from django.urls import path
from .views import PostsList, PostDetail, SearchPage, PostCreate, PostUpdate, PostDelete, ArticleCreate, ArticleUpdate, ArticleDelete, subscriptions

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('search/', SearchPage.as_view(), name='search'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]