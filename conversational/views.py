from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from conversational.forms import ConversationForm, MessageForm, ThoughtForm, SearchConversationForm, SearchMessageForm
from conversational.models import Conversation, Message, Thought


def index(request):
    conversation_list = Conversation.objects.order_by('datetime')
    template = loader.get_template('conversational/index.html')
    form = ConversationForm()
    searchconversation = SearchConversationForm()
    searchmessage = SearchMessageForm()
    context = {
        'conversation_list': conversation_list,
        'form': form,
        'searchconversationform': searchconversation,
        'searchmessageform': searchmessage
    }
    return HttpResponse(template.render(context, request))


def detail(request, conversation_id):
    messageform = MessageForm()
    thoughtform = ThoughtForm()

    try:
        conversation = Conversation.objects.get(pk=conversation_id)
    except Conversation.DoesNotExist:
        raise Http404("Conversation does not exist")
    return render(request, 'conversational/detail.html',
                  {'conversation': conversation,
                   'messageform': messageform,
                   'thoughtform': thoughtform,
                   })


def addmessage(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    form = MessageForm(request.POST)
    if form.is_valid():
        newmessage = Message()
        newmessage.text = form.cleaned_data['text']
        newmessage.datetime = form.cleaned_data['text']
        newmessage.conversation = conversation
        newmessage.save()

        messageform = MessageForm()
        thoughtform = ThoughtForm()

        return render(request, 'conversational/detail.html', {'conversation': conversation,
                                                              'messageform': messageform,
                                                              'thoughtform': thoughtform})


def addthought(request, conversation_id, message_id):
    message = get_object_or_404(Message, pk=message_id)
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    form = ThoughtForm(request.POST)
    if form.is_valid():
        newthought = Thought()
        newthought.text = form.cleaned_data['text']
        newthought.datetime = form.cleaned_data['date']
        newthought.message = message

        newthought.save()

        messageform = MessageForm()
        thoughtform = ThoughtForm()

        return render(request, 'conversational/detail.html', {'conversation': conversation,
                                                              'messageform': messageform,
                                                              'thoughtform': thoughtform})


def addconversation(request):
    form = ConversationForm(request.POST)
    if form.is_valid():
        conversation = Conversation()
        conversation.title = form.cleaned_data['title']
        conversation.datetime = form.cleaned_data['date']
        conversation.save()

        return HttpResponseRedirect(reverse('index'))


def searchconversationtitles(request):
    searchconversation = SearchConversationForm(request.POST)
    if searchconversation.is_valid():
        searchterm = searchconversation.cleaned_data['searchterm']
        queryset = Conversation.objects.filter(title__icontains=searchterm)
        context = {
            'queryset': queryset,
        }
        template = loader.get_template('conversational/conversationsearch.html')
        return HttpResponse(template.render(context, request))


def searchmessagetext(request):
    searchmessage = SearchMessageForm(request.POST)
    if searchmessage.is_valid():
        searchterm = searchmessage.cleaned_data['searchterm']
        queryset = Message.objects.filter(text__icontains=searchterm)
        context = {
            'queryset': queryset,
        }
        template = loader.get_template('conversational/messagesearch.html')
        return HttpResponse(template.render(context, request))
