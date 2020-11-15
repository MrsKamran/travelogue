from django.urls import path
from . import views
from .views import PostCreate


urlpatterns = [
  path('', views.home, name='home'),
  path('index/', views.index, name="index" ),
  path('index/<int:posts_id>/', views.posts_detail, name='detail'),
  path('index/create/', views.PostCreate.as_view(), name='posts_create'),
  path('index/<int:posts_id>/add_review/', views.add_review, name='add_review'),
  path('index/<int:posts_id>/add_photo/', views.add_photo, name='add_photo'),

]