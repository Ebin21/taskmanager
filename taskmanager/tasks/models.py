from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project
from django.urls import reverse

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:task_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Update project status after saving the task
        self.update_project_status()

    def update_project_status(self):
        tasks = self.project.tasks.all()
        total_tasks = tasks.count()
        if total_tasks == 0:
            self.project.status = 'planning'
        else:
            done_tasks = tasks.filter(status='done').count()
            in_progress_tasks = tasks.filter(status='in_progress').count()
            todo_tasks = tasks.filter(status='todo').count()
            
            if done_tasks == total_tasks:
                # All tasks done => project completed
                self.project.status = 'completed'
            elif in_progress_tasks > 0:
                # Any task in progress => project active
                self.project.status = 'on_process'
            elif todo_tasks == total_tasks:
                # All tasks To Do => project planning
                self.project.status = 'active'
            else:
                # Default or other mixed status
                self.project.status = 'active'
        
        self.project.save()
