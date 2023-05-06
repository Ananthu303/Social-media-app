from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    profile_img=models.ImageField(null=True,blank=True,default='blank-profile-picture.png')
    location=models.CharField(max_length=200,blank=True)
    followers=models.ManyToManyField(User,related_name='followers',blank=True,null=True)
    following=models.ManyToManyField(User,related_name='following',blank=True,null=True)
    

    def __str__(self):
        return self.user.__str__() #or .username





class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    image=models.ImageField(null=True,blank=True)
    caption=models.TextField(blank=True)
    posted=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name='likes')
    
    

    def __str__(self):
        return self.caption

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    message=models.TextField()
    posted=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message