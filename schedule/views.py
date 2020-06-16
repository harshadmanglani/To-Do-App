from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.views.generic import ListView, UpdateView, DeleteView, DetailView

from .models import *
from .forms import *

def login_user(request):
    if request.user.is_authenticated:
        return redirect('base')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('base')
            else:
                messages.info(request, 'Username or Password is incorrect')

        return render(request, 'schedule/login.html')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('base')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'Account was created for {user}')
                return redirect('login')

        context = {
            'form':form
        }
        return render(request, 'schedule/register.html', context)

@login_required(login_url='login')
def base(request):

    user = request.user
    tasks = Task.objects.filter(task_user=user)
    # tasks = Task.objects.all()
    form = TaskForm()

    if request.method == 'POST':
        task = Task(task_user=request.user, title=request.POST['title'])
        if task is not None:
            task.save()
            return redirect('base')

        # form = TaskForm(request.POST)
        # print(form.is_valid())
        # if form.is_valid():
        #     form.save()
        #     return redirect('base')

    context = {
        'tasks':tasks,
        'form':form,
    }

    return render(request, 'schedule/base.html', context)

@login_required(login_url='login')
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    context = {
        'form':form,
    }

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('base')

    return render(request, 'schedule/update_task.html', context)

@login_required(login_url='login')
def delete_task(request, pk):
    item = Task.objects.get(id=pk)

    context = {
        'item':item,
    }

    if request.method == 'POST':
        item.delete()
        return redirect('base')

    return render(request, 'schedule/delete.html', context)
