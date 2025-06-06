from django.urls import path
from .views import (PostListView, PostDetailView, PostCreateView,
                    PostUpdateView, PostDeleteView, UserPostListView,
                    PostAgreeView, PostDisagreeView, TopListView, PostCommentView)

urlpatterns = [
    path('', PostListView.as_view(), name='main-home'),
    path('top/', TopListView.as_view(), name='top-posts'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

    path('post/<int:pk>/agree/', PostAgreeView, name='post-agree'),
    path('post/<int:pk>/disagree/', PostDisagreeView, name='post-disagree'),
    path('post/<int:pk>/comment/', PostCommentView, name='post-comment'),
]
