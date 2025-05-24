from django.shortcuts import render,redirect

# Create your views here.


def show_chats_to_operator(request):
    return render(request,'realtime_chat/realtime_chat.html')