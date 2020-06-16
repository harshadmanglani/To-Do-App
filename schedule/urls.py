from django.urls import path, include
from . import views

urlpatterns = [
    #auth
    path('', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('list/', views.base, name='base'),
    path('update_task/<str:pk>/', views.update_task, name='update_task'),
    path('delete_task/<str:pk>/', views.delete_task, name='delete_task'),
]
