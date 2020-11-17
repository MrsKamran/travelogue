from django.forms import ModelForm
from .models import Reviews
from django import forms
class ReviewsForm(ModelForm):
  class Meta:
    model = Reviews
    fields = ['content']
    unlabelled_fields = ['content']
    widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter a review here'}),
        }
    labels = {
           'content' : '',
        }
        
    

