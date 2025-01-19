from django.shortcuts import render

# Create your views here.
def donation(request):
    return render(request,"donations/donation.html")
