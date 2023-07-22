from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('room/<str:pk>/',views.room, name="room"),
    path('profile/<str:pk>' , views.userProfile, name="user_profile"),
    path('create-room/' , views.createRoom, name="createRoom"),
    path('topics/' , views.topics, name="topicView"),
    path('feed/' , views.feed, name="feedView"),
    path('update-room/<str:pk>',views.updateRoom,  name="updateRoom"),
    path('update-user/<str:pk>',views.profileUpdate,  name="updateUser"),
    path('delete-room/<str:pk>',views.deleteRoom,  name="deleteRoom"),
    path('delete-msg/<str:pk>',views.deleteMessage,  name="delete_message")
]
