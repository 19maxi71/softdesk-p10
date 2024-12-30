from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, IssueViewSet, CommentViewSet, UserRegistrationView, delete_user_data

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'issues', IssueViewSet, basename='issue')

# Nested router for comments under issues
issues_router = routers.NestedDefaultRouter(router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(issues_router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('delete-account/', delete_user_data, name='delete_account'),
]
