from django.urls import path
from todoapp import views

app_name = 'todoapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks_list, name='tasks_list'),
    path('task/<int:id>/', views.single_task, name='task'),
    path('new_task/', views.new_task, name='new_task'),
    path('update_task/<int:id>/', views.update_task, name='update_task'),
    path('mark_complete/<int:id>/', views.mark_as_completed, name='mark_complete'),
    path('mark_incomplete/<int:id>', views.mark_as_incomplete, name='mark_incomplete'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
]
