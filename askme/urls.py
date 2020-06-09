from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.main, name='index'),
    path('hot/', views.best_questions, name='hot'),
    path('tag/<slug:cur_tag>/', views.tag_questions, name='tag'),
    path('question/<int:qid>/', views.question, name='question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
]
