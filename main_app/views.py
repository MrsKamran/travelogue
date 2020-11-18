from django.shortcuts import render, redirect
import uuid
import boto3
from .models import Posts, Photo, Reviews, DestinationMarker
from .forms import ReviewsForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.shortcuts import reverse
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
from django.http import JsonResponse

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

class PostCreate(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title', 'city', 'country', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'city', 'country', 'content']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/index/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

class ReviewUpdate(UpdateView):
    model = Reviews
    fields = '__all__'
    success_url = '/index/'

class ReviewDelete(DeleteView):
    model = Reviews
    success_url= '/index/'

def index(request):
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
    if (posts.user != request.user):
        destinationMarker= DestinationMarker.objects.get(post=posts_id)
        markerPositionLat= float(destinationMarker.latitude)
        markerPositionLng= float(destinationMarker.longitude)
        return render(request, 'detail.html', { 'posts': posts, 'reviews_form': reviews_form, 'weather':weather, 'markerPositionLat':markerPositionLat,'markerPositionLng':markerPositionLng,'posts_id':posts_id })
    if (posts.user == request.user):
        return render(request, 'detail.html', { 'posts': posts, 'reviews_form': reviews_form, 'weather':weather, 'posts_id':posts_id })


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

def user_index(request, posts_id, user=None):
        post_owner = Posts.objects.get(id=posts_id).user_id
        posts = Posts.objects.filter(user=post_owner)
        count_posts = Posts.objects.filter(user=post_owner).count()
        reviews = Reviews.objects.filter(user=post_owner)
        count_reviews = Reviews.objects.filter(user=post_owner).count()
        photo = Photo.objects.filter(id=posts_id)
        return render(request, 'user_index.html', {'posts': posts, 'count_posts': count_posts, 'count_reviews': count_reviews,'reviews': reviews, 'photo': photo, 'posts1_id': posts_id})

def add_profile_photo(request, posts_id):
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
            photo1 = Photo(url=url, posts_id=posts_id)
            photo1.save()
        except:
            print('An error occurred uploading file to S3')

    return redirect('user_index', posts_id=posts_id)


def saveDestinationOnMap(request, posts_id):
    posts = Posts.objects.get(id=posts_id)
    if request.is_ajax():
        markerPosition = json.load(request)['markerPosition']
        destinationMarker = DestinationMarker(latitude=markerPosition["lat"],longitude=markerPosition["lng"],post=posts)
        destinationMarker.save()
        return JsonResponse({'markerPosition':markerPosition})
  
