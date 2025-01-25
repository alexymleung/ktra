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
                messages.error(request, '使用者名稱及電郵均已使用')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, '使用者名稱已經使用')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, '電郵已經使用')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, 
                    password=password, 
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name) 
                user.save()
                messages.success(request, "你已成功登記")
                return redirect('login')
        else:
            messages.error(request, '密碼不相符')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.GET.get('message'):
        messages.warning(request, request.GET.get('message'))
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,"你已成功登入")
            return redirect('profile')
        else:
            messages.error(request,"錯誤輸入")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, '你已成功登出')
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


