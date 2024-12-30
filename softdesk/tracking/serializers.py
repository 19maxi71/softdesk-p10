from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment

"""
Serializers pour les modèles User, Project, Contributor, Issue et Comment.
Basé sur la classe ModelSerializer de Django REST Framework.
"""

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'age', 'can_be_contacted', 'can_data_be_shared', 'has_consented']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        if data.get('age') is not None and data['age'] < 15:
            raise serializers.ValidationError("Doit être âgé de 15 ans ou plus.")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            age=validated_data['age'],
            can_be_contacted=validated_data.get('can_be_contacted', False),
            can_data_be_shared=validated_data.get('can_data_be_shared', False),
            has_consented=validated_data.get('has_consented', False)
        )
        return user

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