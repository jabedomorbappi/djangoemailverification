from django.urls import path
from . import views
from .views import youtube_video_view,datepicker

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signup_view, name='signup'),
     path('home', views.home, name='home'),
    
    path('login', views.login_view, name='login'),
    path('verify-email/', views.verify_email, name='verify-email'),
    path('verify-email/done/', views.verify_email_done, name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/', views.verify_email_complete, name='verify-email-complete'),
    path('datepick/', datepicker, name='datepick'),
    path('youtube/<int:video_index>/', youtube_video_view, name='youtube_video'),
    path('youtube/', youtube_video_view, {'video_index': 0}, name='youtube_default'),  # Default to the first video
    path('custom-form/', views.custom_view, name='custom_form'),
    path('success/', views.success_view, name='success_page'),
    
    path('feedback/', views.feedback_view, name='feedback_form'),
    path('success_/', views.success_view_, name='success_page_'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('employee', views.index,name='employee')
    # other paths
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)