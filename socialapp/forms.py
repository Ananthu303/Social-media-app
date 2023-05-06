from django.forms import ModelForm,Widget
from .models import *

class Profileeditform(ModelForm):
    class Meta:
        model=Profile
        fields='__all__'
        exclude=['followers','following',]


class UserModelForm(ModelForm):
    class Meta:
        model=User
        fields=['username']
    
   


# class UploadpostForm(ModelForm):
#     class Meta:
#         model=Post
#         fields='user'
#         exclude=['likes','caption','image']


