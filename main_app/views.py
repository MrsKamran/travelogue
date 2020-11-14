from django.shortcuts import render
import uuid
import boto3
from .models import Posts, Photo
from django.views.generic.edit import CreateView




#This is the Amazon S3 Add A Photo View
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'travelogue1'

def add_photo(request, cat_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        session = boto3.Session(profile_name='dev')
        dev_s3_client = session.client('s3')
        # s3 = boto3.client('s3')
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

def home(request):
    #This code gets the last 3 posts in the list
    posts = Posts.objects.all().order_by('-id')[:3]
    return render(request, 'home.html', {'posts': posts})

class PostCreate(CreateView):
    model = Posts
    fields = ['title', 'city', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def index(request):
    #This code gets the last 3 posts in the list
    posts = Posts.objects.all()
    return render(request, 'index.html', {'posts': posts})