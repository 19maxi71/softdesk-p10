from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import User, Project, Contributor, Issue, Comment
from .serializers import (
    UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
)
from .permissions import IsCreatorOrReadOnly, IsContributorOrReadOnly

# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View pour afficher les utilisateurs. 
    Seuls les administrateurs peuvent effectuer des opérations CRUD.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ProjectViewSet(viewsets.ModelViewSet):
    """
    View pour gérer les opérations CRUD pour les projets.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]

    def get_queryset(self):
        """
        Restreindre l'accès aux projets créés ou auxquels l'utilisateur contribue.
        """
        user = self.request.user
        return Project.objects.filter(creator=user) | Project.objects.filter(contributors__user=user)

    def perform_create(self, serializer):
        """
        Lors de la création d'un projet, attribuer automatiquement le créateur au user connecté.
        """
        serializer.save(creator=self.request.user)

class ContributorViewSet(viewsets.ModelViewSet):
    """
    View pour gérer les opérations CRUD pour les contributeurs.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

class IssueViewSet(viewsets.ModelViewSet):
    """
    View pour gérer les opérations CRUD pour les issues.
    """
    serializer_class = IssueSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(project__contributors__user=user)

    """
    Lors de la création d'une issue, vérifier si 
    l'utilisateur assigné est un contributeur du projet.
    """
    def perform_create(self, serializer):
        assigned_to = self.request.data.get('assigned_to')
        project = serializer.validated_data.get('project')
        
        if assigned_to and not Contributor.objects.filter(user_id=assigned_to, project=project).exists():
            raise serializers.ValidationError("L'utilisateur assigné doit être un contributeur du projet.")
        
        serializer.save(created_by=self.request.user)
        

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(issue__project__contributors__user=user)

    def perform_create(self, serializer):
        issue = serializer.validated_data['issue']
        if not Contributor.objects.filter(user=self.request.user, project=issue.project).exists():
            raise serializers.ValidationError("Vous n'êtes pas un contributeur du projet.")
        serializer.save(author=self.request.user)
