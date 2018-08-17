
from django.conf.urls import url
from . import views    
app_name = 'Login'     
urlpatterns = [
    url(r'^$', views.index, name='index')  ,
    url(r'create_user$', views.create_user, name='create_user')  ,
    url(r'login_user$', views.login_user)  ,
    url(r'success$', views.success, name='home')  ,
    url(r'post_message$', views.create_message, name='create_message')  ,
    url(r'post_comment$', views.create_comment, name='create_comment')  ,
   
]                       