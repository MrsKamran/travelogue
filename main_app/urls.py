from django.urls import path
from . import views
from .views import PostCreate, SearchResultsView


urlpatterns = [
  path('', views.home, name='home'),
  path('search/', SearchResultsView.as_view(), name='search_results'),
  path('index/', views.index, name="index" ),
  path('index/<int:posts_id>/user/', views.user_index, name="user_index" ),
  path('index/<int:posts_id>/user/add_profile_photo/', views.add_profile_photo, name='add_profile_photo'),
  path('index/<int:posts_id>/', views.posts_detail, name='detail'),
  path('index/create/', views.PostCreate.as_view(), name='posts_create'),
  path('index/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
  path('index/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),
  path('index/<int:posts_id>/add_review/', views.add_review, name='add_review'),
  path('index/<int:pk>/reviewupdate/', views.ReviewUpdate.as_view(), name='reviews_update'),
  path('index/<int:pk>/reviewdelete/', views.ReviewDelete.as_view(), name='reviews_delete'),
  path('index/<int:posts_id>/add_photo/', views.add_photo, name='add_photo'),
  # path('markDestinationOnMap', views.markDestinationOnMap),
  path('<int:posts_id>/saveDestinationOnMap', views.saveDestinationOnMap),  
  # path('showDestinationOnMap', views.showDestinationOnMap)
  
]