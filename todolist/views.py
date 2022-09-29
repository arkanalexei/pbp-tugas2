from ast import Delete
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from todolist.models import Task
from todolist.forms import TaskForm
from todolist.forms import UpdateForm



# Create your views here.
@login_required(login_url='/todolist/login/')
def update_task(request, task_id):
	queryset = Task.objects.get(id=task_id)
	form = UpdateForm(instance=queryset)
	if request.method == 'POST':
		form = UpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('todolist:show_todolist')

	context = {
		'form':form
		}

	return render(request, 'update_task.html', context)

@login_required(login_url='/todolist/login/')
def delete_task(request,task_id):
    queryset = Task.objects.get(id=task_id)
    if request.method == 'POST':
        queryset.delete()
        return redirect('todolist:show_todolist')
    
    context = {
        'task':queryset
    }
    return render(request, 'delete_task.html', context)



@login_required(login_url='/todolist/login/')
def show_todolist(request):
    tasks = Task.objects.filter(user=request.user)
    context = {
        'username': request.COOKIES['username'],
        'last_login': request.COOKIES['last_login'],
        'tasks': tasks,
    }
    return render(request, "todolist.html", context)


@login_required(login_url='/todolist/login/')
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            todolist = form.save(commit=False)
            todolist.user = request.user
            todolist.save()
            return redirect('todolist:show_todolist')

    
    form = TaskForm()

    context = {"forms": form,}

    return render(request, 'create_task.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')
    
    context = {'form':form, 'user':request.user}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("todolist:show_todolist")) # membuat response
            response.set_cookie('username', username)
            now = datetime.datetime.now()
            response.set_cookie('last_login', now.strftime("%b. %d, %Y %H:%M:%S")) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('last_login')
    return redirect('todolist:login')