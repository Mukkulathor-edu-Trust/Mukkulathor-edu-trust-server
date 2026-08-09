from django.contrib import admin
from .models import Student, EnrollmentRequest


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'roll_number', 'mobile_number', 'email')
    search_fields = ('full_name', 'student_id', 'roll_number', 'mobile_number', 'email')
    readonly_fields = ('student_id', 'roll_number')


@admin.register(EnrollmentRequest)
class EnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile_number', 'status', 'enrollment_id', 'roll_number', 'created_at', 'approved_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'mobile_number', 'enrollment_id', 'roll_number', 'email')
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        approved = 0
        for enrollment in queryset.filter(status=EnrollmentRequest.STATUS_PENDING):
            enrollment.approve()
            approved += 1

        self.message_user(request, f"{approved} enrollment request(s) approved.")
    approve_requests.short_description = 'Approve selected enrollment requests'
