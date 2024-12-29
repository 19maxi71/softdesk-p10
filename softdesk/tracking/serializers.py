from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment

"""
Serializers pour les modèles User, Project, Contributor, Issue et Comment.
Basé sur la classe ModelSerializer de Django REST Framework.
"""

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'can_be_contacted', 'can_data_be_shared', 'has_consented']
    
    """
    Méthode pour valider l'âge de l'utilisateur.
    """
    def validate(self, data):
        if data.get('age') is not None and data['age'] < 15:
            raise serializers.ValidationError("Doit être âgé de 15 ans ou plus.")
        return data

class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'creator', 'created_time']

class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    project = serializers.StringRelatedField()
    
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']

class IssueSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'assigned_to','nature', 'priority', 'status', 'created_by', 'created_at']
        read_only_fields = ['uuid', 'created_by', 'created_at', 'updated_at'] # Champs en lecture seule

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'uuid', 'issue', 'author', 'content', 'created_at']
    
    """
    Lors de la création d'un commentaire, 
    vérifier si le contenu n'est pas vide.
    """
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Fo écrire quelque chose.")
        return value