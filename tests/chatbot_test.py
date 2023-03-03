# Unit tests for the chatbot


import unittest
from chat import ChatBot
from personalities import *
from modules import *


class TestChatBot(unittest.TestCase):
    def test_chatbot(self):
        chatbot = ChatBot(
            personality=WaldiePersonality(),
            modules=[
                WebSearchModule(),
            ],
            ignore_warnings=True,
            key = "test"
        )

