from django.test import TestCase
from django.urls import reverse
from user_management.models import CustomUser

class IndexViewTest(TestCase):
    def setUp(self):
        # Provide the required arguments for create_user
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpass',
            first_name='Test',
            last_name='User'
        )
        self.url = reverse('index')

    def test_index_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_logged_in(self):
        self.client.login(username='testuser@example.com', password='testpass')  # Log in the user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Should redirect if logged in

    def test_index_view_post_request(self):
        response = self.client.post(self.url, {'field1': 'value1', 'field2': 'value2'})  # Adjust with your form fields
        # Check the response code or any other aspects of the response

    def test_index_view_post_valid_data(self):
        form_data = {
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'New',
            'last_name': 'User',
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())

    def test_index_view_post_invalid_data(self):
        form_data = {
            'email': 'invaliduser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Invalid',
            'last_name': 'User',
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email='invaliduser').exists())
