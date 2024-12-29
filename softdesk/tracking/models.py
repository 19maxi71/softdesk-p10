import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


# Custom user model basé sur abstract class de DRF
class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    has_consented = models.BooleanField(default=False)

    
class Project(models.Model):
    
    """
    Model pour les projets.
    """
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contributor(models.Model):
    """
    Model pour les contributeurs.
    Avec des roles.
    """
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('CONTRIBUTOR', 'Contributor'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CONTRIBUTOR')
    
    class Meta:
        unique_together = ('user', 'project') # Un utilisateur ne peut être qu'une seule fois contributeur d'un projet

    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.role})"

class Issue(models.Model):
    """
    Model pour les issues.
    """
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_issues')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    nature = models.CharField(max_length=20, choices=[
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task')
    ], default='BUG')
    priority = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ], default='LOW')
    status = models.CharField(max_length=20, choices=[
        ('TO_DO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished')
    ], default='TO_DO')

    def __str__(self):
        return f"{self.title} - {self.project.title}"

class Comment(models.Model):
    """
    Model pour les commentaires.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"
