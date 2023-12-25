from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('profile/<int:pk>', Profile.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/<int:user_id>', delete, name='delete'),
    path('update/<int:pk>', UserView.as_view(), name='update'),
    path('profile/<int:pk>/post/create', PostCreate.as_view(), name='post_create'),
    path('profile/<int:pk>/comment/create/<int:post_id>', CommentCreate.as_view(), name='comment_create'),
    path('profile/<int:pk>/comment/commented/create/<int:comment_id>', CommentCommentedView.as_view(), name='comment_commented'),
    path('comment/update/<int:pk>', CommentUpdate.as_view(), name='comment_update'),
    path('comment/delete/<int:comment_id>', delete_comment, name='comment_delete'),
    path('comment/commented/update/<int:pk>', CommentCommentedUpdate.as_view(), name='comment_commented_update'),
    path('comment/commented/delete/<int:comment_id>', delete_comment_commented, name='delete_comment_commented'),
]
