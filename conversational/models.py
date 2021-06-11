
from django.db import models
from django.utils.timezone import now


class Conversation(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField(default=now)

    def __str__(self):
        return self.title


class Message(models.Model):
    text = models.CharField(max_length=500)
    datetime = models.DateTimeField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Thought(models.Model):
    text = models.CharField(max_length=500)
    datetime = models.DateTimeField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
