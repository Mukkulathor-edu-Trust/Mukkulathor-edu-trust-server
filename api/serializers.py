from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, EnrollmentRequest

User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {field.name: {'required': False} for field in model._meta.fields}


class EnrollmentRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = EnrollmentRequest
        fields = '__all__'
        read_only_fields = ('user', 'status', 'enrollment_id', 'roll_number', 'created_at', 'approved_at')

    def validate_mobile_number(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with this mobile number already exists.')
        if EnrollmentRequest.objects.filter(mobile_number=value, status=EnrollmentRequest.STATUS_PENDING).exists():
            raise serializers.ValidationError('An enrollment request with this mobile number is already pending.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        mobile = validated_data.pop('mobile_number')
        email = validated_data.get('email', '')

        user = User.objects.create_user(username=mobile, email=email)
        user.is_active = False
        user.set_password(password)
        user.save()

        enrollment = EnrollmentRequest.objects.create(user=user, mobile_number=mobile, **validated_data)
        return enrollment