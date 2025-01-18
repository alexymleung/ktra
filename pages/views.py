from django.shortcuts import render, get_object_or_404
from events.models import Event
from .models import IndexImage
# Create your views here.
def index(request):
    hero_image = get_object_or_404(IndexImage,name="hero")
    index_imageset = IndexImage.objects.all()
    queryset_event = Event.objects.order_by('-publish_date')[:3]
    context = {
        'hero_image':hero_image,
        'imageset':index_imageset,
        'events':queryset_event
    }
    return render(request,'pages/index.html',context)

def about(request):
    return render(request,'pages/about.html')

def custom_404(request,exception):
    return render(request, 'pages/404.html', status=404)

def custom_500(request):
    return render(request,'pages/500.html',status=500)