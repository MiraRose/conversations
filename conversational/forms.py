import datetime

from django import forms


class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class ConversationForm(forms.Form):
    title = forms.CharField(label='Title', max_length=150)
    date = forms.DateField(initial=datetime.date.today(), label='Start Date', widget=forms.SelectDateWidget)


class MessageForm(forms.Form):
    text = forms.CharField(label='Text', max_length=500)
    date = forms.DateTimeField(initial=datetime.datetime.now(), label='Date/Time', widget=DateInput(), input_formats='')


class ThoughtForm(forms.Form):
    text = forms.CharField(label='Text', max_length=500)
    date = forms.DateTimeField(initial=datetime.datetime.now(), label='Date/Time', widget=DateInput(), input_formats='')


class SearchConversationForm(forms.Form):
    searchterm = forms.CharField(label='Search Conversations by Title', max_length=150)


class SearchMessageForm(forms.Form):
    searchterm = forms.CharField(label='Search Messages by Content', max_length=150)
