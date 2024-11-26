# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'projects', ProjectViewSet, basename='project')
# router.register(r'contributors', ContributorViewSet, basename='contributor')
# router.register(r'issues', IssueViewSet, basename='issue')
# router.register(r'comments', CommentViewSet, basename='comment')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, IssueViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'issues', IssueViewSet, basename='issue')

# Nested router for comments under issues
issues_router = routers.NestedDefaultRouter(router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(issues_router.urls)),
]
