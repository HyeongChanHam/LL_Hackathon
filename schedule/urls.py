from django.urls import path,include
from .views import index,create,time_detail,enrollment,delete,content_detail,password

urlpatterns=[
    path('',index,name='index'),
    path('create/',create,name='create'),
    path('time_detail/<int:content_id>/',time_detail,name='time_detail'),
    path('enrollment/<int:timeslot_id>/',enrollment,name='enrollment'),
    path('password/<int:timeslot_id>/',password,name='password'),
    # path('advise/<int:timeslot_id>/',advise,name='advise'),
    path('delete/<int:timeslot_id>/',delete,name='delete'),
    path('content_detail/<int:content_id>',content_detail,name='content_detail'),
]