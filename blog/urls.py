from django.urls import path
from . import views

urlpatterns = [
    path('trip-inspirations/', views.blog, name='blog'),
    path('trip-inspirations/<int:slug>/', views.blog_post, name='blog_post'),
]