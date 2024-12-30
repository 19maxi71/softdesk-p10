from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers, generics
from .models import User, Project, Contributor, Issue, Comment
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
)
from .permissions import IsCreatorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View pour afficher les utilisateurs. 
    Seuls les administrateurs peuvent effectuer des opérations CRUD.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser, IsAuthenticated]

class SetPagination(PageNumberPagination):
    """
    Pagination pour les projets(5 par page, jusqu'au 20 maximum). 
    Exigence 'GREEN CODE'.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    View pour gérer les opérations CRUD pour les projets. Et la pagination.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]
    pagination_class = SetPagination

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
    
    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if self.request.user != project.creator:
            raise serializers.ValidationError("Seul le créateur du projet peut ajouter des contributeurs.")
        serializer.save()


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
        issue_id = self.kwargs['issue_pk']
        return Comment.objects.filter(issue_id=issue_id, issue__project__contributors__user=self.request.user)

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        if not Contributor.objects.filter(user=self.request.user, project=issue.project).exists():
            raise serializers.ValidationError("Vous n'êtes pas un contributeur du projet.")
        serializer.save(author=self.request.user, issue=issue)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_data(request):
    """
    Supprimer un utilisateur et toutes ses données associées.(Droit à l'oubli)
    """
    user = request.user
    user.delete()
    return Response({"message": "Votre compte a été supprimé. Bye-Bye!"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_sensitive_data(request):
    """ 
    Traitement de consentement pour les données sensibles afin de respecter RGPD.
    """
    if not request.user.has_consented:
        return Response({"error": "Vous devez donner votre consentement pour cette action."}, status=status.HTTP_403_FORBIDDEN)
    
    # Traitement des données sensibles ici
    return Response({"message": "Données traitées avec succès."}, status=status.HTTP_200_OK)
