from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import EnrollmentRequest, Student

User = get_user_model()


class EnrollmentRequestAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )

    def test_create_enrollment_request_creates_inactive_user(self):
        payload = {
            'mobile_number': '9999999999',
            'password': 'TestPass123!',
            'full_name': 'Test Student',
            'aadhar_number': '123456789012',
            'email': 'student@example.com',
            'address': '123 Main St',
        }

        response = self.client.post('/api/enrollment-requests/', payload, format='json')
        self.assertEqual(response.status_code, 201)

        enrollment = EnrollmentRequest.objects.get(mobile_number='9999999999')
        self.assertEqual(enrollment.status, EnrollmentRequest.STATUS_PENDING)
        self.assertEqual(enrollment.full_name, 'Test Student')

        user = enrollment.user
        self.assertEqual(user.username, '9999999999')
        self.assertEqual(user.email, 'student@example.com')
        self.assertFalse(user.is_active)

    def test_admin_can_approve_enrollment_request(self):
        user = User.objects.create_user(
            username='9999999998',
            email='student2@example.com',
            password='TestPass123!'
        )
        user.is_active = False
        user.save()

        enrollment = EnrollmentRequest.objects.create(
            user=user,
            mobile_number='9999999998',
            full_name='Test Student Two',
            aadhar_number='987654321098',
            email='student2@example.com',
            address='456 Main St',
            date_of_birth='2000-01-01',
        )

        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(f'/api/enrollment-requests/{enrollment.pk}/approve/')
        self.assertEqual(response.status_code, 200)

        enrollment.refresh_from_db()
        self.assertEqual(enrollment.status, EnrollmentRequest.STATUS_APPROVED)
        self.assertIsNotNone(enrollment.approved_at)

        user.refresh_from_db()
        self.assertTrue(user.is_active)

        student = Student.objects.filter(user=user).first()
        self.assertIsNotNone(student)
        self.assertEqual(student.student_id, enrollment.enrollment_id)
