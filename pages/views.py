from django.shortcuts import render
from events.models import Event
# Create your views here.
def index(request):
    queryset_event = Event.objects.order_by('-publish_date')[:3]
    context = {
        'events':queryset_event
    }
    return render(request,'pages/index.html',context)

def about(request):
    return render(request,'pages/about.html')

def custom_404(request,exception):
    return render(request, 'pages/404.html', status=404)

def custom_500(request):
    return render(request,'pages/500.html',status=500)