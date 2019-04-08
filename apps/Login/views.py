from django.shortcuts import render, HttpResponse, redirect
from apps.Login.models import *
from django.contrib import messages

def index(request):
    if 'first_name' not in request.session:
        request.session['first_name'] = ''
    if 'last_name' not in request.session:
        request.session['last_name'] = ''
    if 'email' not in request.session:
        request.session['email'] = ''        
    if 'current_first_name' not in request.session:
        request.session['current_first_name'] = ''         
    return render(request,'Login/index.html')
def create_user(request):
    response = User.objects.basic_validator(request.POST)
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request,error)
        print(messages.error)
        return redirect('/login')
    else:
        request.session['user_id'] = response['user_id']      
        return redirect('login/success')     
def login_user(request):
    response = User.objects.login_validator(request.POST)
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request,error)
        return redirect('/login')
    else:
        request.session['user_id'] = response['user_id']      
        return redirect('login/success')    
def success(request): 
    request.session['current_first_name'] = User.objects.get(id=request.session['user_id']).first_name
    current_mess = Message.objects.all()
    current_comm = Comment.objects.all()
    return render(request,'Login/home.html', {'current_mess':current_mess,'current_comm':current_comm})
def create_message(request):
    c = User.objects.get(id = request.session['user_id'])
    Message.objects.create(message=request.POST['message'], message_uploader=c)
    return redirect('login/success')
def create_comment(request):
    c = User.objects.get(id = request.session['user_id'])
    b = Message.objects.get(id = request.POST['message_id'])
    Comment.objects.create(comment=request.POST['comment'], comment_uploader=c,comment_message=b)
    return redirect('login/success')