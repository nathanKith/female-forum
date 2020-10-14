from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='index'),
    path('hot/', views.best_questions, name='hot'),
    path('tag/<slug:cur_tag>/', views.tag_questions, name='tag'),
    path('question/<int:qid>/', views.question, name='question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('logout/', views.logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
