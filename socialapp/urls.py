from django.urls import path
from .views import *
urlpatterns=[
    path('',index,name='index'),
    path('feed/',feed,name='feed'),
    path('home/',home,name='home'),



    path('reg/',register,name='reg'),
    path('login/',loginuser,name='login'),
    path('logout/',logout_view,name='logout'),
    path('profile/<int:id>',profile,name='view-profile'),
    path('profile-edit/<int:id>',profileedit,name='profile-edit'),
    path('upload-post/',uploadpost,name='upload-post'),
    path('edit-post/<int:id>',editpost,name='edit-post'),
    path('delete-post/<int:id>',deletepost,name='delete-post'),
    path('like-post/<int:id>',likepost,name='like-post'),
    path('like-post-home/<int:id>',likeposthome,name='like-post-home'),
    path('follow/<int:id>',follow,name='follow'),
    path('comments/<int:id>',comments,name='comments'),
    path('delete-comment/<int:id>',deletecomment,name='delete-comment'),
   
    



]