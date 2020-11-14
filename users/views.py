from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib.messages import constants as messages


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # message.success(request, f'Account has been created, you are now able to login!')
            return redirect('login')
    else: 
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

