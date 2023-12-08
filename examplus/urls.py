from django.urls import path 

from . import views

app_name = 'examplus'

urlpatterns = [ 
    path("", views.login_view, name = 'login'),
    path("candidate/dashboard", views.candidate_view, name = 'candidate/dashboard'),
    path("invigilator/dashboard", views.invigilator_view, name = 'invigilator/dashboard'),
    path("examiner/dashboard", views.faculty_examiner_view, name = 'examiner/dashboard'),
    path("hod/dashboard", views.department_head_view, name = 'hod/dashboard'),
    path("about", views.about, name = 'about'),
    path('login', views.login_view, name = 'login'),
    path('logout', views.logout_view, name = 'logout'),
    path('delete_report/<report_id>', views.delete_report, name = 'delete-report')
]