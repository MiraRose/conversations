import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from conversational.models import Conversation, Message, Thought


def create_conversation(title):
    date = datetime.datetime.now()
    date = make_aware(date)
    return Conversation.objects.create(title=title, datetime=date)


def create_message(text, conversation):
    date = datetime.datetime.now()
    date = make_aware(date)
    return Message.objects.create(text=text, datetime=date, conversation_id=conversation.id)


def create_thought(text, message):
    date = datetime.datetime.now()
    date = make_aware(date)
    return Thought.objects.create(text=text, datetime=date, message_id=message.id)


class ConversationalTests(TestCase):

    def test_index_with_nothing_in_database_returns_correct_message(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No conversations are available. Start one?")

    def test_create_conversation_shows_on_page(self):
        conversation = create_conversation("this is a conversation")
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['conversation_list'],
            [conversation],
        )

    def test_conversation_shows_on_details_page(self):
        conversation = create_conversation("this is a conversation")
        url = reverse('detail', args=(conversation.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a conversation")

    def test_message_shows_on_details_page_with_associated_conversation(self):
        conversation = create_conversation("this is a conversation")
        message = create_message("this is a message", conversation)
        url = reverse('detail', args=(conversation.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a conversation")
        self.assertContains(response, "this is a message")

    def test_thought_shows_on_details_page_with_associated_conversation_and_message(self):
        conversation = create_conversation("this is a conversation")
        message = create_message("this is a message", conversation)
        thought = create_thought("this is a thought", message)
        url = reverse('detail', args=(conversation.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a conversation")
        self.assertContains(response, "this is a message")
        self.assertContains(response, "this is a thought")

    def test_search_conversation_by_title_shows_expected_conversation(self):
        conversation = create_conversation("this is a conversation")
        response = self.client.post('searchconversationtitles', {'searchterm': 'conversation'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a conversation")
