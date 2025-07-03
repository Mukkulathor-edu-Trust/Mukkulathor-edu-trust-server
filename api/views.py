from django.shortcuts import render
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated

# class StudentViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all().order_by('-id')
#     serializer_class = StudentSerializer
#     permission_classes = [IsAuthenticated]





from rest_framework.response import Response
from rest_framework import status

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-id')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Incoming data:", request.data)  # 👈 Add this line
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)  # 👈 Add this line
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
