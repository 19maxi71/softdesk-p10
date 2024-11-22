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
    # permission_classes = [permissions.IsAdminUser]

class ProjectViewSet(viewsets.ModelViewSet):
    """
    View pour gérer les opérations CRUD pour les projets.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly, IsContributorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ContributorViewSet(viewsets.ModelViewSet):
    """
    View pour gérer les opérations CRUD pour les contributeurs.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    # permission_classes = [permissions.IsAuthenticated]

class IssueViewSet(viewsets.ModelViewSet):
    """
    View pour gérer les opérations CRUD pour les 'issues'.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    # permission_classes = [permissions.IsAuthenticated, IsContributorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    View pour gérer les opérations CRUD pour les commentaires.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated, IsContributorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
