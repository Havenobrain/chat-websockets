from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render, redirect
from .models import *
from .serializers import RoomSerializer
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
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
    return render(request, 'base.html')

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

class UserListView(ListView):
    model = Profile
    template_name = 'user_list.html'  
    context_object_name = 'users'

class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'

class EditProfilePageView(UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    fields = ['profile_pic', 'name']

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.request.user.profile.id})

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

def create_message(request):
    current_user = request.user
    
    if current_user.is_authenticated:
        new_message = Message.objects.create(author=current_user, content="Текст вашего сообщения")
        return new_message
    else:
        return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)

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

    # Измените 'tasks' на существующий маршрут
    success_url = reverse_lazy('user_profile')

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
