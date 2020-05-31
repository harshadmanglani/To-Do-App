from django.shortcuts import render, redirect

from .models import *
from .forms import *

# Create your views here.
def base(request):
    tasks = Task.objects.all()
    form = TaskForm()

    context = {
        'tasks':tasks,
        'form':form,
    }

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('base')

    return render(request, 'schedule/base.html', context)

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

def delete_task(request, pk):
    item = Task.objects.get(id=pk)

    context = {
        'item':item,
    }

    if request.method == 'POST':
        item.delete()
        return redirect('base')

    return render(request, 'schedule/delete.html', context)
