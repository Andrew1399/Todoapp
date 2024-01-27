from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from todoapp.models import TodoList
from todoapp.forms import CreateUpdateTaskForm


def index(request):
    return render(request, 'todoapp/index.html')

@login_required
def tasks_list(request):
    tasks = TodoList.objects.filter(user=request.user)
    done_tasks = TodoList.objects.filter(user=request.user, completed=True)
    # search = request.Get.get('search-area') or ''
    # # check
    # if search:
    #     tasks = tasks.filter(title__icontains=search)
    count_tasks = tasks.filter(completed=False).count()
    context = {'tasks': tasks, "done_tasks": done_tasks, 'count_tasks': count_tasks}
    return render(request, 'todoapp/tasks_list.html', context)

@login_required
def single_task(request, id):
    task = get_object_or_404(TodoList, id=id, user=request.user)
    return render(request, 'todoapp/task.html', {'task': task})

@login_required
def new_task(request):
    if request.method != 'POST':
        form = CreateUpdateTaskForm()
    else:
        form = CreateUpdateTaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            if task.completed:
                task.completed = True
            task.save()
        return redirect('todoapp:tasks_list')
    return render(request, 'todoapp/new_task.html', {'form': form})

@login_required
def update_task(request, id):
    task = get_object_or_404(TodoList, id=id, user=request.user)
    if request.method != 'POST':
        form = CreateUpdateTaskForm(instance=task)
    else:
        form = CreateUpdateTaskForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('todoapp:task', id=id)
    return render(request, 'todoapp/update_task.html', {'form': form, 'task': task})

@login_required
def mark_as_completed(request, id):
    task = get_object_or_404(TodoList, id=id)
    task.completed = True
    task.save()
    return redirect('todoapp:tasks_list')

@login_required
def mark_as_incomplete(request, id):
    task = get_object_or_404(TodoList, id=id)
    task.completed = False
    task.save()
    return redirect('todoapp:tasks_list')

@login_required
def delete_task(request, id):
    task = get_object_or_404(TodoList, id=id, user=request.user)
    task.delete()
    return redirect('todoapp:tasks_list')  #or HttpResponseRedirect and reverse_lazy???
