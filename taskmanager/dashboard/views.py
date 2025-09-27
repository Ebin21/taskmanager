from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from projects.models import Project
from tasks.models import Task

@login_required
def dashboard_home(request):
    user = request.user

    # Retrieve projects user is part of or all if admin
    if user.is_superuser or user.role == 'admin':
        projects = Project.objects.all()
        tasks = Task.objects.all()
    else:
        projects = Project.objects.filter(Q(created_by=user) | Q(members=user)).distinct()
        tasks = Task.objects.filter(Q(project__in=projects) | Q(assigned_to=user)).distinct()

    task_stats = {
        'todo': tasks.filter(status='todo').count(),
        'in_progress': tasks.filter(status='in_progress').count(),
        'done': tasks.filter(status='done').count(),
        'total': tasks.count(),
    }

    project_stats = {
        'planning': projects.filter(status='planning').count(),
        'active': projects.filter(status='active').count(),
        'completed': projects.filter(status='completed').count(),
        'total': projects.count(),
    }

    context = {
        'tasks': tasks,
        'projects': projects,
        'task_stats': task_stats,
        'project_stats': project_stats,
    }

    return render(request, 'dashboard/home.html', context)

@login_required
def chart_data(request):
    user = request.user

    if user.is_superuser or user.role == 'admin':
        tasks = Task.objects.all()
    else:
        projects = Project.objects.filter(Q(created_by=user) | Q(members=user)).distinct()
        tasks = Task.objects.filter(Q(project__in=projects) | Q(assigned_to=user)).distinct()

    to_do = tasks.filter(status='todo').count()
    in_progress = tasks.filter(status='in_progress').count()
    done = tasks.filter(status='done').count()

    data = {
        'labels': ['To Do', 'In Progress', 'Done'],
        'datasets': [{
            'data': [to_do, in_progress, done],
            'backgroundColor': ['#ffc107', '#17a2b8', '#28a745'],
            'borderColor': ['#e0a800', '#138496', '#1e7e34'],
            'borderWidth': 1,
        }],
    }

    return JsonResponse(data)
