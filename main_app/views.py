from django.shortcuts import render, redirect
import uuid
import boto3
from .models import Posts, Photo, Reviews
from .forms import ReviewsForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.views.generic import DetailView
from django.contrib.auth.models import User

import os
import requests
from dotenv import load_dotenv
load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


#This is the Amazon S3 Add A Photo View
S3_BASE_URL = 'https://s3.ca-central-1.amazonaws.com/'
BUCKET = 'travelogue2'

def home(request):
    #This code gets the last 3 posts in the list
    posts = Posts.objects.all().order_by('-id')[:3]
    return render(request, 'home.html', {'posts': posts})

class PostCreate(CreateView):
    model = Posts
    fields = ['title', 'city', 'country', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdate(UpdateView):
  model = Posts
  fields = ['title', 'city', 'country', 'content']

class PostDelete(DeleteView):
  model = Posts
  success_url = '/index/'

def index(request):
    #This code gets the last 3 posts in the list
    posts = Posts.objects.all()
    return render(request, 'index.html', {'posts': posts})

def posts_detail(request, posts_id):
    posts = Posts.objects.get(id=posts_id)
    reviews_form = ReviewsForm()
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+WEATHER_API_KEY
    weather_json = requests.get(weather_url.format(posts.city)).json()
    weather = {
            'city' : posts.city,
            'temperature' : weather_json['main']['temp'],
            'description' : weather_json['weather'][0]['description'],
            'icon' : weather_json['weather'][0]['icon']
        }

    return render(request, 'detail.html', { 'posts': posts, 'reviews_form': reviews_form, 'weather':weather })

def add_review(request, posts_id):
     # create a ModelForm instance using the data in request.POST
    form = ReviewsForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the post_id assigned
        new_review = form.save(commit=False)
        new_review.user = request.user
        new_review.posts_id = posts_id
        new_review.save()
    return redirect('detail', posts_id=posts_id)

def add_photo(request, posts_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, posts_id=posts_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', posts_id=posts_id)
    
class SearchResultsView(ListView):
    model = Posts
    template_name = 'search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Posts.objects.filter(
            Q(country__icontains=query) | Q(city__icontains=query)
        )
        return object_list

def user_index(request,posts_id, user=None):
        posts1 = Posts.objects.get(id=posts_id)
        post_owner = posts1.user_id
        posts = Posts.objects.filter(user=post_owner)
        return render(request, 'user_index.html', {'posts': posts})

