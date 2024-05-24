from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render, redirect
from .models import *
from .serializers import RoomSerializer
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



def HomeView(request):
    if request.method == 'POST': 
        username = request.POST['username']
        room = request.POST['room']
        try:
            existing_room = Room.objects.get(room_name__icontains=room)
        except Room.DoesNotExist:
            r = Room.objects.create(room_name=room)
        return redirect('room', room_name=room, username=username)
    return render(request, 'home.html')


def RoomView(request, room_name, username):
    permission_classes = (IsAuthenticatedOrReadOnly)
    existing_room = Room.objects.get(room_name__icontains=room_name)
    get_message = Message.objects.filter(room=existing_room)
    context = {
        'messages': get_message,
        'user': username,
        'room_name': existing_room.room_name,
    }
    return render(request, 'room.html', context)


def create_message(request):
    # Получаем текущего пользователя
    current_user = request.user
    
    # Проверяем, что пользователь аутентифицирован
    if current_user.is_authenticated:
        # Создаем новое сообщение и указываем текущего пользователя как его автора
        new_message = Message.objects.create(author=current_user, content="Текст вашего сообщения")
        # Далее вы можете выполнять другие действия с сообщением или просто его возвращать
        return new_message
    else:
        # Обработка ситуации, когда пользователь не аутентифицирован
        return "Пользователь не аутентифицирован"


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context

class CreateProfilePageView(CreateView):
    model = Profile
    
    template_name = 'create_profile.html'
    fields = ['profile_pic', 'name']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('tasks')




class RoomAPIList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)



class RoomAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)


class RoomAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAdminUser)