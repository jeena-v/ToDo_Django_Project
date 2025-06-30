from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import date
from .models import Task
from .forms import TaskForm
from django.db.models import Q


def signup_view(request):                   #for signup
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'ToDoApp/signup.html', {'form': form})

@login_required                #create-task
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')

        # Handle simple form from task_list
        if title:
            Task.objects.create(user=request.user, title=title, description=description)
            return redirect('task_list')

        # Handle full Django form
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'ToDoApp/task_form.html', {'form': form})
    
from datetime import date

@login_required
def task_list(request):
    user = request.user
    query = request.GET.get('q')                   #search
    filter_val = request.GET.get('filter')
    today_date = date.today()

    # Only count today's uncompleted tasks for My Day
    my_day_tasks = Task.objects.filter(user=user, is_completed=False, created_at__date=today_date)
    my_day_count = my_day_tasks.count()

    tasks_count = Task.objects.filter(user=user).count()
    important_count = Task.objects.filter(user=user, is_important=True, is_completed=False).count()

    if filter_val == 'important':                    #for important task
        if query:
            active_tasks = Task.objects.filter(
                user=user,
                is_completed=False,
                is_important=True
            ).filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by('-created_at')

            completed_tasks = Task.objects.filter(
                user=user,
                is_completed=True,
                is_important=True
            ).filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        else:
            active_tasks = Task.objects.filter(
                user=user,
                is_completed=False,
                is_important=True
            ).order_by('-created_at')

            completed_tasks = Task.objects.filter(
                user=user,
                is_completed=True,
                is_important=True
            )
    else:
        #Show only today's tasks for My Day
        if query:
            active_tasks = Task.objects.filter(
                user=user,
                is_completed=False,
                created_at__date=today_date
            ).filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by('-created_at')

            completed_tasks = Task.objects.filter(
                user=user,
                is_completed=True,
                created_at__date=today_date
            ).filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        else:
            active_tasks = Task.objects.filter(
                user=user,
                is_completed=False,
                created_at__date=today_date
            ).order_by('-created_at')

            completed_tasks = Task.objects.filter(
                user=user,
                is_completed=True,
                created_at__date=today_date
            )

    return render(request, 'ToDoApp/task_list.html', {
        'tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'today': today_date,
        'query': query,
        'filter_val': filter_val,
        'my_day_count': my_day_count,
        'tasks_count': tasks_count,
        'important_count': important_count,
    })

from django.views.decorators.http import require_POST

@require_POST
@login_required                         #for set due-date
def update_due_date(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    due_date = request.POST.get('due_date')
    if due_date:
        task.due_date = due_date
        task.save()
    return redirect('task_list')


@login_required            #for all tasks 
def task_all(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'ToDoApp/task_all.html', {'tasks': tasks})
    
@login_required                  #for update
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'ToDoApp/task_form.html', {'form': form})    


@login_required                            #for Delete
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'ToDoApp/task_confirm_delete.html', {'task': task})


from django.utils import timezone

@login_required                           #for marking completed
def mark_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if not task.is_completed:
        task.is_completed = True
        task.completed_at = timezone.now()  
        task.save()
    return redirect('task_list')


@login_required                               #for marking impotrant 
def toggle_important(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_important = not task.is_important
    task.save()
    return redirect('task_list')