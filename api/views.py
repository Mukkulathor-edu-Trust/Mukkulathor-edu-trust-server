from django.shortcuts import render
from rest_framework import viewsets
from .models import Student, EnrollmentRequest
from .serializers import StudentSerializer, EnrollmentRequestSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-id')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Incoming data:", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EnrollmentRequestViewSet(viewsets.ModelViewSet):
    queryset = EnrollmentRequest.objects.all().order_by('-created_at')
    serializer_class = EnrollmentRequestSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [p() for p in permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        enrollment = self.get_object()
        student = enrollment.approve()
        if student:
            return Response(StudentSerializer(student).data)
        return Response({'detail': 'Enrollment already processed or cannot approve.'}, status=status.HTTP_400_BAD_REQUEST)
