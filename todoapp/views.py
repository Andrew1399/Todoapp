from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from todoapp.models import TodoList
from todoapp.forms import CreateUpdateTaskForm


def index(request):
    return render(request, 'todoapp/index.html')

class CustomLoginView(LoginView):
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todo_list')


class RegisterView(FormView):
    template_name = 'todoapp/register.html'
    form_class = FormView
    redirect_authenticated_user = True
    success_url = 'todo_list'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

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




# class TodoListView(LoginRequiredMixin, ListView):
#     template_name = 'todoapp/todo_list.html'
#     model = TodoList
#     context_object_name = 'tasks'
#     login_url = 'login-page'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tasks'] = context['tasks'].filter(user=self.request.user)
#         context['count'] = context['']
#
# class TaskCreateView(LoginRequiredMixin, CreateView):
#     model = TodoList
#     fields = ['title', 'description', 'completed']
#     success_url = 'todo_list'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(TaskCreateView, self).form_valid(form)


