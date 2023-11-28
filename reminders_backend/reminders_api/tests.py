from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Reminder
import datetime
from .serializers import ReminderSerializer

class ReminderViewTestCase(APITestCase):
  
  def setUp(self):
    # Set up a test account
    self.creator = User.objects.create(
      username='testuser',
      email='testuser@example.com',
      password='AJWDIp32'
    )
    # Authenticate the test account
    self.client.force_authenticate(user=self.creator)
    
    # Create a test reminder
    self.reminder = Reminder.objects.create(
      creator = self.creator,
      content = 'lorem ipsum dolor sit amet lorem ipsum dolor sit',
      expiration_date = datetime.datetime.now() + datetime.timedelta(days=7)
    )
  
  # View Reminders for authenticated user
  def test_get_queryset_authenticated_user(self):
    url = '/api/v1/reminders/'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer_data = ReminderSerializer([self.reminder], many=True).data
    self.assertEqual(response.data, serializer_data)
    
  # View Reminders for unauthenticated user
  def test_get_queryset_unauthenticated_user(self):
    self.client.logout()
    url = '/api/v1/reminders/'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)