from django.db import models
from .fields import EncryptedCharField

class Student(models.Model):
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