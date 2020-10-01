from django import forms
from .models import Content,DateTime,UserTemp
import datetime

class ContentForm(forms.Form):
    creator=forms.CharField(max_length=50)
    creator_key=forms.IntegerField()
    contact=forms.CharField(widget=forms.Textarea)

    title=forms.CharField(max_length=50)
    department=forms.CharField(max_length=50)
    
    date=forms.DateTimeField(initial=datetime.datetime.now())
    runningdate=forms.IntegerField()

    runningtime=forms.IntegerField()
    location=forms.CharField(max_length=50)

    num_people=forms.IntegerField()
    reward=forms.CharField(max_length=50)

    condition=forms.CharField(widget=forms.Textarea)
    detail=forms.CharField(widget=forms.Textarea)

    password=forms.IntegerField()

class PasswordForm(forms.Form):
    password_temp=forms.IntegerField()

class UserTempForm(forms.ModelForm):

    class Meta:
        model=UserTemp
        fields=('name','major','num_student','num_phone','num_account','password')

class TimeMakingForm(forms.ModelForm):
    class Meta:
        model=DateTime
        fields=('starttime','endtime')

class ContentReviseForm(forms.ModelForm):
    class Meta:
        model=Content
        fields=('creator','contact','title','department','reward','condition','detail','location')

