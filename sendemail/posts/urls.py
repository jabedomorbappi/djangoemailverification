from django.contrib import admin 
from django.urls import path

from posts.views import PostsView 
from django.conf import settings 
from django.conf.urls.static import static 
urlpatterns = [
    path('pagination',PostsView.as_view(),name='pagination'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)