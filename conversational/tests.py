import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from conversational.forms import ThoughtForm, ConversationForm, MessageForm
from conversational.views import create_conversation, create_thought, create_message

from conversational.models import Conversation, Message, Thought

mydatetime = datetime.datetime.now()
mydatetime = make_aware(mydatetime)

date = datetime.date.today()


def create_test_conversation(title):
    return Conversation.objects.create(title=title, date=date)


def create_test_message(text, conversation):
    return Message.objects.create(text=text, datetime=mydatetime, conversation_id=conversation.id)


def create_test_thought(text, message):
    return Thought.objects.create(text=text, datetime=mydatetime, message_id=message.id)


class ConversationalTests(TestCase):

    def test_index_with_nothing_in_database_returns_correct_message(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No conversations are available. Start one?")

    def test_conversation_shows_on_page(self):
        conversation = create_test_conversation("this is a conversation")

        response = self.client.get(reverse('index'))

        self.assertQuerysetEqual(
            response.context['conversation_list'],
            [conversation],
        )

    def test_conversation_shows_on_details_page(self):
        conversation = create_test_conversation("this is a conversation")
        url = reverse('detail', args=(conversation.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a conversation")

    def test_message_shows_on_details_page_with_associated_conversation(self):
        conversation = create_test_conversation("this is a conversation")
        message = create_test_message("this is a message", conversation)
        url = reverse('detail', args=(conversation.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a conversation")
        self.assertContains(response, "this is a message")

    def test_thought_shows_on_details_page_with_associated_conversation_and_message(self):
        conversation = create_test_conversation("this is a conversation")
        message = create_test_message("this is a message", conversation)
        thought = create_test_thought("this is a thought", message)
        url = reverse('detail', args=(conversation.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a conversation")
        self.assertContains(response, "this is a message")
        self.assertContains(response, "this is a thought")

    def test_search_conversation_by_title_shows_expected_conversation(self):
        conversation = create_test_conversation("this is a conversation")
        conversation2 = create_test_conversation("redherring")
        url = reverse('searchconversationtitles')

        response = self.client.post(url, {'searchterm': 'this'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a conversation")
        self.assertNotContains(response, "redherring")

    def test_search_message_by_text_shows_expected_message_thought(self):
        conversation = create_test_conversation("this is a conversation")
        message = create_test_message("this is a message", conversation)
        message2 = create_test_message("redherring", conversation)
        thought = create_test_thought("this is a thought", message)
        url = reverse('searchmessagetext')

        response = self.client.post(url, {'searchterm': 'message'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a message")
        self.assertContains(response, "this is a thought")
        self.assertNotContains(response, "redherring")

    def test_post_conversation_show_conversation_on_index_after_posting(self):
        url = reverse('addconversation')

        response = self.client.post(url, {'title': 'this is a conversation', 'date': date}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a conversation")

    def test_post_message_show_message_after_posting(self):
        conversation = create_test_conversation("this is a conversation")
        url = reverse('addmessage', args=(conversation.id,))
        response = self.client.post(url, {'text': 'this is a message', 'date': mydatetime})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a message")

    def test_post_message_show_message_after_posting(self):
        conversation = create_test_conversation("this is a conversation")
        message = create_test_message("this is a message", conversation)
        url = reverse('addthought', args=(conversation.id, message.id))
        response = self.client.post(url, {'text': 'this is a thought', 'date': mydatetime})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is a thought")

    def test_create_thought_has_text_date(self):
        form = ThoughtForm(data={"text": "This is a thought", "date": mydatetime})
        form.is_valid()
        conversation = create_test_conversation("This is a conversation")
        message = create_test_message("This is a message", conversation)
        result_thought = create_thought(form, message)

        self.assertEqual(result_thought.text, "This is a thought")
        self.assertEqual(result_thought.datetime, mydatetime)

    def test_create_conversation_has_title_date(self):
        form = ConversationForm(data={"title": "This is a conversation", "date": date})
        form.is_valid()

        result_conversation = create_conversation(form)

        self.assertEqual(result_conversation.title, "This is a conversation")
        self.assertEqual(result_conversation.date, date)

    def test_create_message_has_text_date(self):
        form = MessageForm(data={"text": "This is a message", "date": mydatetime})
        form.is_valid()
        conversation = create_test_conversation("This is a conversation")

        result_message = create_message(form, conversation)

        self.assertEqual(result_message.text, "This is a message")
        self.assertEqual(result_message.datetime, mydatetime)
