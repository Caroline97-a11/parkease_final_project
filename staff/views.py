from django.shortcuts import render, redirect
from .forms import StaffLoginForm, StaffForm
from .models import Staff
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
def loginPage(request):
    if request.method =='POST':
     form = StaffLoginForm(request, data =request.POST)
     if form.is_valid():
        userDeatils =form.get_user()
        login(request, userDeatils)
        return redirect('loginPage') 
    else:
       form =StaffLoginForm()
    return render(request, 'loginpage.html', {'form':form})
def register(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('loginPage')

    else:
        form = StaffForm()

    return render(request, 'user_registration.html', {'form': form})

