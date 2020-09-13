from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.add_news_article, name='news-add_article'),
    path('<int:link>/', views.news_link, name='news-link'),
    path('', views.main_page, name='news-main'),
]
