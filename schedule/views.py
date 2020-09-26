from django.shortcuts import render,redirect,get_object_or_404
from .models import Content,DateTime,UserTemp
from .forms import ContentForm,UserTempForm,PasswordForm,ContentAdviseForm
from datetime import datetime,timedelta,time,date

# Create your views here.
def index(request):
    all_content=Content.objects.all()
    all_timeslot=DateTime.objects.filter(isUsed=False)
    return render(request,'index.html',{'all_content':all_content,'all_timeslot':all_timeslot})

def create(request):
    if request.method=='POST':
        form=ContentForm(request.POST)
        if form.is_valid():
            obj_content=Content(creator=form.data['creator'],contact=form.data['contact'],title=form.data['title'],department=form.data['department'],location=form.data['location'],reward=form.data['reward'],condition=form.data['condition'],detail=form.data['detail'],password=form.data['password'])
            obj_content.save()
            num_people=int(form.data['num_people'])
            runningdate=int(form.data['runningdate'])
            runningtime=int(form.data['runningtime'])
            date_time=form.data['date']
            for i in range(runningdate):
                date=(datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')+timedelta(days=i)).date()
                dow=date.weekday()
                for j in range(num_people):
                    starttime=(datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')+timedelta(minutes=runningtime*j)).time()
                    endtime=(datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')+timedelta(minutes=runningtime*(j+1))).time()
                    obj_timeslot=DateTime(content=obj_content,date=date,starttime=starttime,endtime=endtime,day_of_week=dow,isUsed=False)
                    obj_timeslot.save()
            return redirect('index')
    content_form=ContentForm()
    return render(request,'create.html',{'content_form':content_form})

def content_detail(request,content_id):
    content=Content.objects.filter(pk=content_id)
    return render(request,'content_detail.html',{'contents':content})

def enrollment(request,timeslot_id):
    if request.method=='POST':
        filled_form=UserTempForm(request.POST)
        if filled_form.is_valid():
            temp_form=filled_form.save(commit=False)
            temp_form.time_temp=DateTime.objects.get(pk=timeslot_id)
            temp_form.save()

            timeslot=DateTime.objects.get(pk=timeslot_id)
            timeslot.isUsed=True
            timeslot.save()

            return redirect('index')

    timeslot=DateTime.objects.get(pk=timeslot_id)
    usertemp=UserTempForm()
    if timeslot.isUsed==False:
        return render(request,'usertemp.html',{'usertemp':usertemp,'timeslot':timeslot.id})
    if timeslot.isUsed==True:
        return redirect('password',timeslot.id)

def time_detail(request,content_id):
    content=get_object_or_404(Content,pk=content_id)
    time_slots=DateTime.objects.all()
    time_slot=time_slots.filter(content=content_id)
    return render(request,'time_detail.html',{'time_slot':time_slot})


def content_admin(request,content_id):
    passwordform=PasswordForm()
    content_id=content_id
    if request.method=="POST":
        passwordform=PasswordForm(request.POST)
        password_temp=passwordform.data['password_temp']
        content=Content.objects.get(pk=content_id)
        if int(content.password)==int(password_temp):
            content=get_object_or_404(Content,pk=content_id)
            time_slots=DateTime.objects.all()
            time_slot=time_slots.filter(content=content_id)
            content_form=ContentAdviseForm(instance=content)
            # if request.method=="POST":
            #     updated_form=ContentAdviseForm(request.POST,instance=content) 
            #     if updated_form.is_valid():
            #         content.title=updated_form.data['title']
            #         content.save()
            #         return redirect('index')
            return render(request,'time_detail_for_creator.html',{'time_slot':time_slot,'content_form':content_form,'content_id':content.id})
        else:
            return render(request,'content_admin.html',{'passwordform':passwordform,'content_id':content_id})
    return render(request,'content_admin.html',{'passwordform':passwordform,'content_id':content_id})

def password(request,timeslot_id):
    passwordform=PasswordForm()
    if request.method=="POST":
        passwordform=PasswordForm(request.POST)
        password_temp=passwordform.data['password_temp']

        timeslot=DateTime.objects.get(pk=timeslot_id)
        try:
            usertemp_obj=UserTemp.objects.get(time_temp=timeslot)
        except:
            return render(request,'password.html',{'passwordform':passwordform})

        if int(usertemp_obj.password)==int(password_temp):
            timeslot=DateTime.objects.get(pk=timeslot_id)
            user=UserTemp.objects.get(time_temp=timeslot)
            usertemp_form=UserTempForm(instance=user)
            # if request.method=="POST":
            #     updated_form=UserTempForm(request.POST,instance=user) 
            #     if updated_form.is_valid():
            #         updated_form.save()
            #         return redirect('index')
            return render(request,'usertemp_advise.html',{'usertemp':usertemp_form,'timeslot':timeslot.id})
        else:
            return render(request,'password.html',{'passwordform':passwordform})
    return render(request,'password.html',{'passwordform':passwordform})

def content_revise(request,content_id):
    content=Content.objects.get(pk=content_id)
    if request.method=="POST":
            updated_form=ContentAdviseForm(request.POST,instance=content) 
            if updated_form.is_valid():
                    content.title=updated_form.data['title']
                    content.contact=updated_form.data['contact']
                    content.title=updated_form.data['title']
                    content.department=updated_form.data['department']
                    content.reward=updated_form.data['reward']
                    content.condition=updated_form.data['condition']
                    content.detail=updated_form.data['detail']
                    content.location=updated_form.data['location']
                    content.save()
                    return redirect('index')

def time_revise(request,timeslot_id):
    timeslot=DateTime.objects.get(pk=timeslot_id)
    user=UserTemp.objects.get(time_temp=timeslot)
    usertemp_form=UserTempForm(instance=user)
    if request.method=="POST":
        updated_form=UserTempForm(request.POST,instance=user) 
        if updated_form.is_valid():
            updated_form.save()
            return redirect('index')    

# def advise(request,timeslot_id):
#     timeslot=DateTime.objects.get(pk=timeslot_id)
#     user=UserTemp.objects.get(time_temp=timeslot)
#     usertemp_form=UserTempForm(instance=user)
#     if request.method=="POST":
#         updated_form=UserTempForm(request.POST,instance=user) 
#         if updated_form.is_valid():
#             updated_form.save()
#             return redirect('index')
#     return render(request,'usertemp_advise.html',{'usertemp':usertemp_form,'timeslot':timeslot.id})

def delete(request,timeslot_id):
    timeslot=DateTime.objects.get(pk=timeslot_id)
    timeslot.isUsed=False
    timeslot.save()
    user=UserTemp.objects.get(time_temp=timeslot)
    user.delete()

    return redirect('index')

def close(request,timeslot_id,content_id):
    if request.method=="POST": 
        content=get_object_or_404(Content,pk=content_id)
        time_slots=DateTime.objects.all()
        time_slot=time_slots.filter(content=content_id)
        content_form=ContentAdviseForm(instance=content)    
        
        timeslot=DateTime.objects.get(pk=timeslot_id)
        if timeslot.isUsed==False:
            timeslot.isUsed=True
            timeslot.save()
        return render(request,'time_detail_for_creator.html',{'time_slot':time_slot,'content_form':content_form,'content_id':content.id})
        


