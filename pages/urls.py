from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contract-terms/', views.terms, name='terms'),
    path('where-to-stay/', views.where, name='where'),
    path('about/', views.about, name='about'),
    path('faqs/', views.faqs, name='faqs'),
]
