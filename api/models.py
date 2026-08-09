import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .fields import EncryptedCharField

User = get_user_model()


def generate_unique_user_id():
    while True:
        code = f"UT{timezone.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        if not EnrollmentRequest.objects.filter(enrollment_id=code).exists() and not Student.objects.filter(student_id=code).exists():
            return code


def generate_unique_roll_number():
    while True:
        code = f"ROLL{timezone.now().strftime('%y%m%d%H%M%S')}{uuid.uuid4().hex[:3].upper()}"
        if not EnrollmentRequest.objects.filter(roll_number=code).exists() and not Student.objects.filter(roll_number=code).exists():
            return code


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    student_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    roll_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    # Personal Information
    full_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    parent_guardian_name = models.CharField(max_length=100, blank=True, null=True)
    student_contact = models.CharField(max_length=15, blank=True, null=True)
    parent_contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # aadhar_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    aadhar_number = EncryptedCharField(max_length=200, unique=True, blank=True, null=True)
    aadhar_photo = models.TextField(blank=True, null=True)

    # Academic Details
    school_college_name = models.CharField(max_length=150, blank=True, null=True)
    class_grade = models.CharField(max_length=50, blank=True, null=True)
    board_university = models.CharField(max_length=100, blank=True, null=True)
    academic_records = models.TextField(blank=True, null=True)
    medium_of_instruction = models.CharField(max_length=50, blank=True, null=True)

    # SSLC
    has_school_sslc = models.BooleanField(default=False, blank=True)
    sslc_board = models.CharField(max_length=50, blank=True, null=True)
    sslc_year = models.CharField(max_length=10, blank=True, null=True)
    sslc_percentage = models.CharField(max_length=10, blank=True, null=True)
    sslc_school = models.CharField(max_length=100, blank=True, null=True)

    # HSC
    has_hsc = models.BooleanField(default=False, blank=True)
    hsc_board = models.CharField(max_length=50, blank=True, null=True)
    hsc_year = models.CharField(max_length=10, blank=True, null=True)
    hsc_percentage = models.CharField(max_length=10, blank=True, null=True)
    hsc_college = models.CharField(max_length=100, blank=True, null=True)
    hsc_stream = models.CharField(max_length=50, blank=True, null=True)

    # UG
    has_ug = models.BooleanField(default=False, blank=True)
    ug_course = models.CharField(max_length=50, blank=True, null=True)
    ug_college = models.CharField(max_length=100, blank=True, null=True)
    ug_year = models.CharField(max_length=10, blank=True, null=True)
    ug_percentage = models.CharField(max_length=10, blank=True, null=True)
    ug_specialization = models.CharField(max_length=100, blank=True, null=True)

    # PG
    has_pg = models.BooleanField(default=False, blank=True)
    pg_course = models.CharField(max_length=50, blank=True, null=True)
    pg_college = models.CharField(max_length=100, blank=True, null=True)
    pg_year = models.CharField(max_length=10, blank=True, null=True)
    pg_percentage = models.CharField(max_length=10, blank=True, null=True)
    pg_specialization = models.CharField(max_length=100, blank=True, null=True)

    # Coaching
    target_exams = models.CharField(max_length=200, blank=True, null=True)
    preferred_subjects = models.CharField(max_length=200, blank=True, null=True)
    preparation_level = models.CharField(max_length=50, blank=True, null=True)
    coaching_package = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    photo = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name if self.full_name else "Student"


class EnrollmentRequest(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, unique=True)
    enrollment_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    roll_number = models.CharField(max_length=50, unique=True, blank=True, null=True)

    full_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    parent_guardian_name = models.CharField(max_length=100, blank=True, null=True)
    student_contact = models.CharField(max_length=15, blank=True, null=True)
    parent_contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    aadhar_number = EncryptedCharField(max_length=200, unique=True, blank=True, null=True)
    aadhar_photo = models.TextField(blank=True, null=True)

    school_college_name = models.CharField(max_length=150, blank=True, null=True)
    class_grade = models.CharField(max_length=50, blank=True, null=True)
    board_university = models.CharField(max_length=100, blank=True, null=True)
    academic_records = models.TextField(blank=True, null=True)
    medium_of_instruction = models.CharField(max_length=50, blank=True, null=True)

    has_school_sslc = models.BooleanField(default=False, blank=True)
    sslc_board = models.CharField(max_length=50, blank=True, null=True)
    sslc_year = models.CharField(max_length=10, blank=True, null=True)
    sslc_percentage = models.CharField(max_length=10, blank=True, null=True)
    sslc_school = models.CharField(max_length=100, blank=True, null=True)

    has_hsc = models.BooleanField(default=False, blank=True)
    hsc_board = models.CharField(max_length=50, blank=True, null=True)
    hsc_year = models.CharField(max_length=10, blank=True, null=True)
    hsc_percentage = models.CharField(max_length=10, blank=True, null=True)
    hsc_college = models.CharField(max_length=100, blank=True, null=True)
    hsc_stream = models.CharField(max_length=50, blank=True, null=True)

    has_ug = models.BooleanField(default=False, blank=True)
    ug_course = models.CharField(max_length=50, blank=True, null=True)
    ug_college = models.CharField(max_length=100, blank=True, null=True)
    ug_year = models.CharField(max_length=10, blank=True, null=True)
    ug_percentage = models.CharField(max_length=10, blank=True, null=True)
    ug_specialization = models.CharField(max_length=100, blank=True, null=True)

    has_pg = models.BooleanField(default=False, blank=True)
    pg_course = models.CharField(max_length=50, blank=True, null=True)
    pg_college = models.CharField(max_length=100, blank=True, null=True)
    pg_year = models.CharField(max_length=10, blank=True, null=True)
    pg_percentage = models.CharField(max_length=10, blank=True, null=True)
    pg_specialization = models.CharField(max_length=100, blank=True, null=True)

    target_exams = models.CharField(max_length=200, blank=True, null=True)
    preferred_subjects = models.CharField(max_length=200, blank=True, null=True)
    preparation_level = models.CharField(max_length=50, blank=True, null=True)
    coaching_package = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    photo = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.enrollment_id:
            self.enrollment_id = generate_unique_user_id()
        if not self.roll_number:
            self.roll_number = generate_unique_roll_number()
        super().save(*args, **kwargs)

    def approve(self):
        if self.status != self.STATUS_PENDING:
            return None

        student = Student.objects.create(
            user=self.user,
            student_id=self.enrollment_id,
            roll_number=self.roll_number,
            mobile_number=self.mobile_number,
            full_name=self.full_name,
            date_of_birth=self.date_of_birth,
            gender=self.gender,
            parent_guardian_name=self.parent_guardian_name,
            student_contact=self.student_contact or self.mobile_number,
            parent_contact=self.parent_contact,
            email=self.email,
            address=self.address,
            aadhar_number=self.aadhar_number,
            aadhar_photo=self.aadhar_photo,
            school_college_name=self.school_college_name,
            class_grade=self.class_grade,
            board_university=self.board_university,
            academic_records=self.academic_records,
            medium_of_instruction=self.medium_of_instruction,
            has_school_sslc=self.has_school_sslc,
            sslc_board=self.sslc_board,
            sslc_year=self.sslc_year,
            sslc_percentage=self.sslc_percentage,
            sslc_school=self.sslc_school,
            has_hsc=self.has_hsc,
            hsc_board=self.hsc_board,
            hsc_year=self.hsc_year,
            hsc_percentage=self.hsc_percentage,
            hsc_college=self.hsc_college,
            hsc_stream=self.hsc_stream,
            has_ug=self.has_ug,
            ug_course=self.ug_course,
            ug_college=self.ug_college,
            ug_year=self.ug_year,
            ug_percentage=self.ug_percentage,
            ug_specialization=self.ug_specialization,
            has_pg=self.has_pg,
            pg_course=self.pg_course,
            pg_college=self.pg_college,
            pg_year=self.pg_year,
            pg_percentage=self.pg_percentage,
            pg_specialization=self.pg_specialization,
            target_exams=self.target_exams,
            preferred_subjects=self.preferred_subjects,
            preparation_level=self.preparation_level,
            coaching_package=self.coaching_package,
            start_date=self.start_date,
            end_date=self.end_date,
            photo=self.photo,
        )

        self.status = self.STATUS_APPROVED
        self.approved_at = timezone.now()
        self.save()
        self.user.is_active = True
        self.user.save()
        self.send_approval_notification()
        return student

    def send_approval_notification(self):
        if not self.user.email:
            return

        subject = 'Your trust enrollment request has been approved'
        message = (
            f"Dear {self.full_name},\n\n"
            f"Your request has been approved. Please visit the trust in person to complete the next steps.\n\n"
            f"Enrollment ID: {self.enrollment_id}\n"
            f"Roll Number: {self.roll_number}\n\n"
            "Thank you for choosing Mukkulathor Free Educational & Employment Trust."
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            fail_silently=True,
        )

    def __str__(self):
        return f"Enrollment request for {self.full_name or self.mobile_number}"
