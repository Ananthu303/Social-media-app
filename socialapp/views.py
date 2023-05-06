from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.http import HttpResponse
from .models import Profile
from .models import *
import os
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
   if request.user.is_authenticated:
      return redirect('home')
   return render(request,'index.html')


@login_required(login_url='login')
def feed(request):  

    user=request.user

    user_model=User.objects.get(username=user)
    pro=Profile.objects.get(user=user_model)

    
    
    post=Post.objects.filter(profile__followers=user).order_by('-posted')
    if not pro.following.exists():
       return redirect('home')

    if not request.user.is_authenticated:
        return redirect('home')

    dp=request.user.profile_set.all()

    

    
    return render(request,'feed.html',{'post':post,'dp':dp,})




def home(request):
   
   post=Post.objects.all().order_by('-posted')
   try:
    user=request.user.profile_set.all()
   except:
    user=0

   
      
   return render(request,'home.html',{'post':post,'user':user})


def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username Already Exists')

        elif User.objects.filter(email=email).exists():
            messages.error(request,'Email Already Exists')

        elif password != cpassword:
            messages.error(request,"Password Mismatch")
        
        else:
            user=User.objects.create(username=username,email=email)
            user.set_password(password)
            user.save()
            profile_obj=Profile.objects.create(user=user)
            profile_obj.save()
            
            return redirect('login')


    return render(request,'registration.html')


def loginuser(request):
    if request.user.is_authenticated:
       return redirect('feed')
    
    if request.method=='POST':
      
      username=request.POST.get('username')
      password=request.POST.get('password')

      try:
         user=User.objects.get(username=username)
      except:
         messages.error(request,'User not found')
     
    
 
      user=authenticate(request,username=username,password=password)

      if user is not None:
         login(request,user)
         return redirect('feed')

        
    return render(request,'login.html')




def logout_view(request):
    logout(request)
    return redirect('index')





def profile(request,id):

   user=User.objects.get(id=id)
   post_count=user.post_set.all().count()
   user_profile=user.profile_set.all()
   post=user.post_set.all()
  
   try:
     cu=request.user.profile_set.all()
    
   except:
    cu= None

   return render(request,'profile.html',{'profile':user_profile,'post_count':post_count,'cu':cu,'post':post})
   

@login_required(login_url='login')   
def profileedit(request,id):
   user_obj=User.objects.get(id=id)
   profile=Profile.objects.get(user=user_obj)
   user=request.user.profile_set.all()
   
   

  
   if request.method== 'POST':
       try:
        image=request.FILES['image']
       except:
          pass
       bio=request.POST.get('bio')
       location=request.POST.get('location')
       try:
        if len(image)>0 :
           os.remove(profile.profile_img.path)
           profile.profile_img=image
       except:
        pass
       profile.bio=bio
       profile.location=location
       a=profile.user
       a.username=request.POST.get('username')
       a.save()
       profile.save()
       return redirect('view-profile',id=user_obj.id)
    

         
 

       
    
  
   return render(request,'profile-edit.html',{'pro':profile,'req_user':user})




@login_required(login_url='login')  
def uploadpost(request):
    user=User.objects.get(username=request.user)
    profile=Profile.objects.get(user=user)
    current_user=request.user.profile_set.all()
    
    if request.method == 'POST':
      image=request.FILES['image']
      caption=request.POST.get('caption')
      Post.objects.create(user=user,image=image,caption=caption,profile=profile)
      return redirect('home') 
    return render(request,'upload-post.html',{'user':profile,'req_user':current_user})








@login_required(login_url='login')   
def editpost(request,id):
    post=Post.objects.get(id=id)
    
    if request.method=='POST':
        try:
         post.image=request.FILES['image']
        except:
         pass
        post.caption=request.POST.get('caption')
        post.save()
        return redirect('home')

    return render(request,'edit-post.html',{'post':post,})



@login_required(login_url='login')   
def deletepost(request,id):
    post=Post.objects.get(id=id)
    if request.method =='POST':
        post.delete()
        return redirect('home')

    return render(request,'delete-post.html',{'post':post})




@login_required(login_url='login')   
def likepost(request,id):


    post=Post.objects.get(id=id)
    
    if post.likes.filter(username=request.user).exists():
        post.likes.remove(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        post.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))





@login_required(login_url='login')   
def likeposthome(request,id):


    post=Post.objects.get(id=id)
    
    if post.likes.filter(username=request.user).exists():
        post.likes.remove(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        post.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    




@login_required(login_url='login')      
def follow(request,id):
    user=User.objects.get(id=id) #to get the profile user model
    profile=Profile.objects.get(user=user)

    req_user=User.objects.get(username=request.user) #to get our profilemodel
    current_user=Profile.objects.get(user=req_user)


    if profile.followers.filter(username=request.user).exists():
        profile.followers.remove(request.user)
        current_user.following.remove(user)
        
        return redirect('view-profile', id=user.id)
        
    else:
        profile.followers.add(request.user)
        current_user.following.add(user)
       
        return redirect('view-profile',id=user.id)
        


 
def comments(request,id):
    
  
   post=Post.objects.get(id=id)
   the_post_comments=post.comments_set.all()
   

   count=post.comments_set.all().count()
   
   if request.user.is_authenticated:
    user=User.objects.get(username=request.user)
    profile=Profile.objects.get(user=user)
   else:
      user=0
      profile=0
   

   message=request.POST.get('message')
   if request.method =='POST':
      the_comment=Comments.objects.create(user=request.user,profile=profile,post=post,message=message)   

      return redirect('comments',id=post.id)
   
   return render(request,'comments.html',{'comments':the_post_comments,'count':count,'profile':profile,})


@login_required(login_url='login')  
def deletecomment(request,id):
  
  comment=Comments.objects.get(id=id)
  post_id=comment.post.id
  comment.delete()
  return redirect('comments',id=post_id)
  
 


   

   


   
   



