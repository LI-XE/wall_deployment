from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('post_message', views.post_message),
    path('post_comment/<int:post_id>', views.post_comment),
    path('user_profile/<int:user_id>', views.profile),
    path('post_message/<int:post_id>/delete', views.delete),
    path('like/<int:post_id>', views.add_like)
]