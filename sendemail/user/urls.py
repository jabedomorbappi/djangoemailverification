from django.urls import path
from . import views
from .views import youtube_video_view,datepicker


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
   
]