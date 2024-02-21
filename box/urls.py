
from django.contrib.auth import views as auth_views
from django.urls import path

from box import views

urlpatterns = [
    path('',views.home,name='home'),
    
    #  auth
    path('signup',views.SignUp.as_view(),name='signup'),
    path('login',auth_views.LoginView.as_view(),name='login'),
    path('logout',views.LogOut.as_view(),name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    
    #box
    path('box/create/',views.CreateBox.as_view(), name='create_box'),
    path('box/<str:pk>/update/',views.UpdateBox.as_view(), name='update_box'),
    path('box/<str:pk>/delete/',views.DeleteBox.as_view(), name='delete_box'),
    path('box/<str:pk>/',views.DetailBox.as_view(), name='detail_box'),
    path('list/',views.ListBox.as_view(), name='list_box'),
    
    # videos
    path('box/<str:pk>/addvideo/',views.addVideo,name='add_video'),
    
    
]