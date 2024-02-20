from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note

class NoteAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_user_signup(self):
        signup_data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('register'), signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser2').exists())
        print("Test 'User Signup'.")

    def test_user_login(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 'User Login'.")

    def test_create_note(self):
        note_data = {
            'title': 'Test Note',
            'content': 'This is a test note content.'
        }
        response = self.client.post(reverse('create-new-note'), note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Note.objects.filter(title='Test Note').exists())
        print("Test 'Create Note'.")

    def test_retrieve_note_list(self):
        response = self.client.get(reverse('create-new-note'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 'Retrieve Note List'.")

    def test_retrieve_note_detail(self):
        note = Note.objects.create(title='Test Note', content='This is a test note content.', owner=self.user)
        response = self.client.get(reverse('rud-on-notes', kwargs={'pk': note.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 'Retrieve Note Detail'.")

    def test_update_note(self):
        note = Note.objects.create(title='Test Note', content='This is a test note content.', owner=self.user)
        updated_note_data = {
            'title': 'Updated Test Note',
            'content': 'This is an updated test note content.'
        }
        response = self.client.put(reverse('rud-on-notes', kwargs={'pk': note.id}), updated_note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_note = Note.objects.get(id=note.id)
        self.assertEqual(updated_note.title, 'Updated Test Note')
        self.assertEqual(updated_note.content, 'This is an updated test note content.')
        print("Test 'Update Note'.")

    def test_delete_note(self):
        note = Note.objects.create(title='Test Note', content='This is a test note content.', owner=self.user)
        response = self.client.delete(reverse('rud-on-notes', kwargs={'pk': note.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(id=note.id).exists())
        print("Test 'Delete Note'.")

    def test_share_note(self):
        note = Note.objects.create(title='Test Note', content='This is a test note content.', owner=self.user)
        another_user = User.objects.create_user(username='anotheruser', email='another@example.com', password='testpassword')
        share_note_data = {
            'users': [another_user.username]
        }
        response = self.client.post(reverse('share-notes-with-other-users', kwargs={'pk': note.id}), share_note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shared_users = note.shared_users.all()
        self.assertIn(another_user, shared_users)
        print("Test 'Share Note'.")

    def test_version_history(self):
        note = Note.objects.create(title='Test Note', content='This is a test note content.', owner=self.user)
        updated_note_data = {
            'title': 'Updated Test Note',
            'content': 'This is an updated test note content.'
        }
        self.client.put(reverse('rud-on-notes', kwargs={'pk': note.id}), updated_note_data, format='json')
        response = self.client.get(reverse('get-notes-history', kwargs={'id': note.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
        print("Test 'Version History'.")
