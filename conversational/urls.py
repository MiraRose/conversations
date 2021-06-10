from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:conversation_id>/', views.detail, name='detail'),
    path('<int:conversation_id>/addmessage/', views.addmessage, name='addmessage'),
    path('<int:conversation_id>/<int:message_id>/addthought/', views.addthought, name='addthought'),
    path('addconversation/', views.addconversation, name='addconversation'),
    path('searchconversationtitles/', views.searchconversationtitles, name='searchconversationtitles'),
    path('searchmessagetext/', views.searchmessagetext, name='searchmessagetext'),
]
