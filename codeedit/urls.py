from django.urls import path

from . import views

urlpatterns = [
    path('<int:task_id>/', views.show_task, name='show_task'),
    path('check/<int:task_id>/', views.check_task, name='check_task'),
    path('check/<int:task_id>/<int:test_id>', views.run_test, name='run_test'),
    path('', views.list_tasks, name='list_tasks'),
]