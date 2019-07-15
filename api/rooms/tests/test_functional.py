### FUNCTIONAL TESTS
from django.test import LiveServerTestCawse

from selenium.webdriver.firefox.webdriver import WebDriver


class NewVisitorTest(TestCase):

    @classmethod
    def setUpClass(cls):
        self.setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass()(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_can_start_a_new_chat_room(self):
        """
        User starts a new chat room.
        """
        # User goes to home page
        # User sees two options - start a new room or enter room hash
        # User starts a new chat room - sees an empty chat room with the first message as the new hash
        # User posts in the room
        # User sees post
        pass

    def test_can_enter_an_existing_chat_room_and_post(self):
        ## User goes to existing chat room and posts
        # User goes to home page
        # User sees two options - start a new room or enter room hash
        # User enters a room hash and gets redirected to the chat page
        # User sees chats from before
        # User posts in the room
        # User sees post
        pass
