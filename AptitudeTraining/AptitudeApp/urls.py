"""
URL configuration for AptitudeTraining project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.login),
    path('signup',views.signup),
    path('adminhome',views.adminhome),
    path('changepassword',views.changepassword),
    path('addeducontent',views.addeducontent),
    path('vieweducontent',views.vieweducontent),
    path('updateeducontent/<id>',views.updateeducontent),
    path('deleteeducontent/<id>',views.deleteeducontent),
    path('addquestion',views.addquestion),
    path('viewquestions',views.viewquestions),
    path('updatequestion/<id>',views.updatequestion),
    path('deletequestion/<id>',views.deletequestion),
    path('viewfeedbacks',views.viewfeedbacks),
    path('viewcomplaints',views.viewcomplaints),
    path('sentreply/<id>',views.sentreply),
    path('logout',views.logout, name='logout'),
    path('index1',views.index1),
]
