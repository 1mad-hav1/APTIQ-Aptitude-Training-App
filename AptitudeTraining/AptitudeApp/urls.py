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
    path('adminlearnmore/', views.admin_learn_more, name='admin_learn_more'),
    path('changepassword',views.changepassword),
    path('addeducontent',views.addeducontent),
    path('vieweducontent',views.vieweducontent),
    path('get_video_links/<int:id>/', views.get_video_links),
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
    path('and_user_registration',views.and_user_registration),
    path('and_login',views.and_login),
    path('and_user_profile',views.and_user_profile),
    path('and_sent_feedback',views.and_sent_feedback),
    path('and_view_feedbacks',views.and_view_feedbacks),
    path('and_user_change_password',views.and_user_change_password),
    path('and_user_update_profile',views.and_user_update_profile),
    path('and_get_study_material',views.and_get_study_material),
    path('and_get_detailed_content',views.and_get_detailed_content),
    path('and_get_test_questions',views.and_get_test_questions),
    path('and_post_test_results',views.and_post_test_results),
    path('and_get_test_result',views.and_get_test_result),
    path('and_get_results',views.and_get_results),
    path('and_get_section_test_questions',views.and_get_section_test_questions),
    path('and_post_section_test_results',views.and_post_section_test_results),
]
