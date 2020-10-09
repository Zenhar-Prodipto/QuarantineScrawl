from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib import  messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
#All the messages

# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error
 
# Create your views here.
def register(request):
    if request.method== 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('home')

    else:
        form = UserRegistrationForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):

    return render(request,'users/profile.html')