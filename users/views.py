from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.messages import constants as messages
from django.contrib.auth.decorators import login_required



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

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else: 
         u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/update.html', {'u_form': u_form})
 
    