from django.urls import path,reverse

from . import views

#app_name = 'employee'

urlpatterns = [
    path('', views.index, name='index'),
    path('records', views.records, name='records'),
    path('post', views.post, name='post'),
    path('update', views.update, name='update'),
    path('sync', views.sync, name='sync'),
]