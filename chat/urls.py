from django.urls import path, include
from .views import *
from rest_framework import routers




urlpatterns = [
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/room', RoomAPIList.as_view()),
    path('api/v1/room/<int:pk>/', RoomAPIUpdate.as_view()),
    path('api/v1/roomdelete/<int:pk>/', RoomAPIDestroy.as_view()),
    path('account/profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    path('create_profile_page/',CreateProfilePageView.as_view(), name='create_user_profile'),
    path('', HomeView, name='login'),
    path('<str:room_name>/<str:username>/', RoomView, name='room'),
]

