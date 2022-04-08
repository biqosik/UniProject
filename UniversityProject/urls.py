from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    path('blockchain/<str:pk>/', views.blockchainFeed, name="cryptocurrency"),
    path('topics/', views.topicPage, name="topic-page"),
    path('activity/', views.activityPage, name="activity-page"),
    path('conversation/', views.conversationPage, name="conversation"),
    path('news/', views.newsPage, name="news-page"),
    path('crypto/', views.cryptoPage, name="crypto-page"),
    path('blockchain/', views.blockchainPage, name="blockchain"),
]
