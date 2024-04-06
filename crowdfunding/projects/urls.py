from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('exams/', views.ExamList.as_view()),
    path('exams/<int:pk>/', views.ExamDetail.as_view()),
    path('tutor_projects/', views.ProjectList.as_view()),
    path('tutor_projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('tutor_pledges/', views.PledgeList.as_view()),
    path('tutor_pledges/<int:pk>/', views.PledgeDetailView.as_view()),
    path('', views.HelloWorld.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)