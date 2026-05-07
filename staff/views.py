from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import HttpResponseForbidden
from django.contrib import messages

from .forms import StaffLoginForm, StaffForm
from .models import Staff


# =========================
# LOGIN
# =========================
def loginPage(request):
    if request.method == 'POST':
        form = StaffLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            role = user.role

            if role == "ADMIN":
                return redirect('report_dashboard')

            elif role == "ATTENDANT":
                return redirect('dashboard')

            elif role == "MANAGER":
                return redirect('service_price_list')

            return redirect('/')

    else:
        form = StaffLoginForm()

    return render(request, 'loginPage.html', {'form': form})


# =========================
# ACCESS DENIED
# =========================
def no_access():
    return HttpResponseForbidden("You do not have permission to access this page.")


# =========================
# REGISTER USER (ADMIN ONLY)
# =========================
def register(request):
    if not request.user.is_authenticated:
        return redirect('loginPage')

    if request.user.role != 'ADMIN':
        return no_access()

    if request.method == 'POST':
        form = StaffForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = StaffForm()

    return render(request, 'user_registration.html', {'form': form})


# =========================
# LOGOUT
# =========================
def logout_user(request):
    logout(request)
    return redirect('loginPage')


# =========================
# USER LIST (ADMIN ONLY)
# =========================
def user_list(request):
    if not request.user.is_authenticated:
        return redirect('loginPage')

    if request.user.role != 'ADMIN':
        return no_access()

    users = Staff.objects.all().order_by("-date_joined")

    return render(request, "user_list.html", {"users": users})


# =========================
# EDIT USER (ADMIN ONLY)
# =========================
def edit_user(request, pk):
    if not request.user.is_authenticated:
        return redirect('loginPage')

    if request.user.role != 'ADMIN':
        return no_access()

    user = get_object_or_404(Staff, id=pk)

    if request.method == 'POST':
        form = StaffForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = StaffForm(instance=user)

    return render(request, 'edit_user.html', {'form': form})


# =========================
# DELETE USER (ADMIN ONLY)
# =========================
def delete_user(request, id):
    if not request.user.is_authenticated:
        return redirect('loginPage')

    if request.user.role != 'ADMIN':
        return no_access()

    user = get_object_or_404(Staff, id=id)

    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('user_list')

    return render(request, 'delete_user.html', {'user': user})