from django.urls import reverse

from rest_framework.test import APITestCase, APIRequestFactory

from rooms.models import Chatroom, Message


class ChatroomAPIEndpointTestCase(APITestCase):
    def test_create_chatroom(self):
        """
        Check if chatroom object can be created.
        """
        url = reverse('chatroom-list')
        data = {
            'name': 'Test room',
        }
        response = self.client.post(url, data, format='json')
        
        # Make sure room was created, exists and props are as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Chatroom.objects.count(), 1)
        self.assertEqual(Chatroom.objects.first().name, 'Test room')

    def test_list_chatrooms(self):
        """
        Check if we can list chatrooms.
        """
        # Make chatrooms
        url = reverse('chatroom-list')
        data = [
            {
                'name': 'Test room',
            },
            {
                'name': 'Test room 2',
            }
        ]
        for json in data:
            self.client.post(url, json, format='json')

        response = self.client.get(url)

        # Make sure rooms are listed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test room')
        self.assertContains(response, 'Test room 2')

    def test_patch_chatroom(self):
        """
        Check if we can update chatroom name.
        """
        # Create room
        self.client.post(
            reverse('chatroom-list'), {'name': 'Test room raw',}, format='json'
        )

        room = Chatroom.objects.first()
        
        # Build request
        url = reverse('chatroom-detail', kwargs={'pk': room.hash})
        data = {
            'name': 'Test room updated',
        }
        
        response = self.client.patch(
            url, data, format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Chatroom.objects.count(), 1)
        self.assertEqual(Chatroom.objects.first().name, 'Test room updated')

    def test_retrieve_chatroom(self):
        """
        Test chatroom detail.
        """
        self.client.post(
            reverse('chatroom-list'), {'name': 'Test room',}, format='json'
        )
        hash = Chatroom.objects.first().hash
        
        response = self.client.get(
            reverse('chatroom-detail', kwargs={'pk': hash})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test room')

    def test_destroy_chatroom(self):
        """
        Check if we can delete chatroom.
        """
        self.client.post(
            reverse('chatroom-list'), {'name': 'Test room',}, format='json'
        )
        hash = Chatroom.objects.first().hash
        
        response = self.client.delete(
            reverse('chatroom-detail', kwargs={'pk': hash})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Chatroom.objects.count(), 0)


class MessageAPIEnpointTestCase(APITestCase):
    def setUp(self):
        self.client.post(
            reverse('chatroom-list'), {'name': 'Test room',}, format='json'
        )
        self.hash = Chatroom.objects.first().hash

    def test_create_message(self):
        """
        Check if message object can be created.
        """
        url = reverse(
            'message-list', kwargs={'hash': self.hash}
        )
        data ={
            'author': 'Me',
            'message': 'This is a test message.'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().message, 'This is a test message.')

    def test_list_messages(self):
        """
        Check if we can list messages.
        """
        # Make chatrooms
        url = reverse(
            'message-list', kwargs={'hash': self.hash}
        )
        data = [
            {
                'author': 'Me',
                'message': 'This is a test message.'
                },
            {
                'author': 'Me',
                'message': 'This is a test message 2.'
            }
        ]
        for json in data:
            self.client.post(url, json, format='json')

        response = self.client.get(url)

        # Make sure rooms are listed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test message.')
        self.assertContains(response, 'This is a test message 2.')

    def test_retrieve_message(self):
        # Make message
        self.client.post(
            reverse('message-list', kwargs={'hash': self.hash}),
            {
                'author': 'Me',
                'message': 'This is a test message.'
            },
            format='json'
        )

        message_id = Message.objects.first().pk

        # Get message
        url = reverse(
            'message-detail', kwargs={'hash': self.hash, 'id': message_id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test message.')
