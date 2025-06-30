from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('task/<int:task_id>/complete/', views.mark_completed, name='mark_completed'),
    path('all/', views.task_all, name='task_all'),
    path('task/<int:task_id>/update_due_date/', views.update_due_date, name='update_due_date'),
    path('toggle-important/<int:task_id>/', views.toggle_important, name='toggle_important'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='ToDoApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]