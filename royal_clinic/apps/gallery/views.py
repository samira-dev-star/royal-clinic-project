from django.shortcuts import render,get_list_or_404
from .models import ServiceVideo
# Create your views here.


def video_list(request):
    
    videos = ServiceVideo.objects.all()[:3]
    
    context = {
        'videos': videos,
    }
    
    return render(request, 'gallery/partials/gallery_partials.html', context)

# ----------------------------------------------------------------------

def video_list_all(request):
    
    videos = ServiceVideo.objects.all()
    
    context = {
        'videos': videos,
    }
    
    return render(request, 'gallery/all_videos.html', context)

# ----------------------------------------------------------------------

def specific_video(request, pk):
    
    video = get_list_or_404(ServiceVideo, pk=pk)
    
    context = {
        'video': video,
    }
    
    return render(request, 'partials/gallery_partials.html', context)