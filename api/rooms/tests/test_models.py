from django.test import TestCase

from rooms.models import Chatroom, Message


class ChatroomTestCase(TestCase):
    def setUp(self):
        self.room = Chatroom.objects.create(
            name='Test room'
        )

        # assign messages
        author = 'Jane Doe'
        messages = [
            'Test message 1',
            'Test message 2'
        ]

        for i in range(2):
            Message.objects.create(
                chatroom=self.room,
                author=author,
                message=messages[i]
            )

    def test_can_make_room(self):
        chatroom = Chatroom.objects.create(
            name='Test room 2'
        )

        self.assertIsInstance(chatroom, Chatroom)

    def test_get_messages(self):
        messages = self.room.get_messages()

        self.assertEqual(messages.count(), 2)

        # Last added is posted last (see get_messages)
        self.assertEqual(messages.first().message, 'Test message 2')
        self.assertEqual(messages.last().message, 'Test message 1')

    def test_str(self):
        self.assertEqual(f'{self.room.name} - ({self.room.hash})', self.room.__str__())

    def test_as_dict(self):
        self.assertEqual(
            {
                'hash': self.room.hash,
                'name': self.room.name,
                'created_at': self.room.created_at,
                'last_posted': self.room.last_posted
            },
            self.room.as_dict()
        )


class MessageTestCase(TestCase):
    def setUp(self):
        self.room = Chatroom.objects.create(
            name='Test room'
        )

        # assign messages
        author = 'Jane Doe'
        message = 'Test message 1'

        self.message = Message.objects.create(
            author=author, message=message, chatroom=self.room
        )

    def test_str(self):
        self.assertEqual(
            f'Message in {self.message.chatroom.name}({self.message.chatroom.hash}) by {self.message.author} - {self.message.posted_at}',
            self.message.__str__()
        )
    
    def test_as_dict(self):
        self.assertEqual(
            {
                'id': self.message.pk,
                'chatroom': self.message.chatroom,
                'author': self.message.author,
                'message': self.message.message,
                'posted_at': self.message.posted_at,
            },
            self.message.as_dict()
        )
