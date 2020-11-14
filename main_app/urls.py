from django.urls import path
from . import views
from .views import PostCreate


urlpatterns = [
  path('', views.home, name='home'),
  path('index/', views.index, name="index" ),
  path('index/create/', views.PostCreate.as_view(), name='posts_create'),

]