from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, EnrollmentRequestViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'enrollment-requests', EnrollmentRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
