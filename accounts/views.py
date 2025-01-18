from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.db.models import Q
from django.contrib.auth.models import User
from bookings.models import Booking
from django.db.models import Count, F, Sum

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(Q(username=username) & Q(email=email)).exists():
                messages.error(request, 'Both username and email taken already, please try again')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username taken already, please try again')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email taken already, please try again')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, 
                    password=password, 
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name) 
                user.save()
                messages.success(request, "Your registration is successful. Please proceed to log in")
                return redirect('login')
        else:
            messages.error(request, 'Passwords not matched')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,"You have logged in")
            return redirect('profile')
        else:
            messages.error(request,"Invalid credentials, please log in again")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You have logged out!')
    return redirect('index')

def profile(request):
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(user_id=request.user.id).select_related('service', 'user')
        user_bookings = user_bookings.values(
            'service_id',
            'service__title',
            'service__fee',
            'user__username').annotate(
                count=Count('service_id'),
                total_fee=Sum('service__fee')
                ).order_by('service_id')
        context = {
            'user_bookings':user_bookings
        }
        return render(request,'accounts/profile.html',context)
    else:
        return redirect("login")


