from django.urls import path
from . import views
from .views import student_info_view, mark_attendance_view, success_view, view_percentage
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', LoginView.as_view(template_name='leave_app/login.html'), name='home'),  # Make /login/ the homepage
    path('dashboard/', LoginView.as_view(template_name='leave_app/dashboard.html'), name='dashboard'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mark-attendance/', mark_attendance_view, name='mark_attendance'),
    path('success/', success_view, name='success_url'),
    path('view-percentage/', view_percentage, name='view_percentage'),
    path('select-page/', views.select_page, name='select_page'),
    path('student-info/', student_info_view, name='student_info'),
    path('display_student_info/', views.display_student_info, name='display_student_info'),
    path('leave-requests/', views.leave_requests, name='leave_requests'),
    path('process-leave/<int:leave_id>/<str:action>/', views.process_leave, name='process_leave'),
    path('leave-status/', views.leave_status, name='leave_status'),
]


# Add this line outside of the urlpatterns list
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
