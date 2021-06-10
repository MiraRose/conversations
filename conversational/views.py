from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from conversational.models import Conversation, Message, Thought


def index(request):
    conversation_list = Conversation.objects.order_by('datetime')
    template = loader.get_template('conversational/index.html')
    context = {
        'conversation_list': conversation_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, conversation_id):
    try:
        conversation = Conversation.objects.get(pk=conversation_id)
    except Conversation.DoesNotExist:
        raise Http404("Conversation does not exist")
    return render(request, 'conversational/detail.html', {'conversation': conversation})


def addmessage(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    try:
        newmessage = Message()
        newmessage.text = request.POST['newmessage']
        newmessage.datetime = request.POST['messagedate']
        newmessage.conversation = conversation
    except (KeyError, Conversation.DoesNotExist):
        return render(request, 'conversational/detail.html', {
            'conversation': conversation,
            'error_message': "Something went wrong.",
        })
    else:
        newmessage.save()

        return render(request, 'conversational/detail.html', {'conversation': conversation})


def addthought(request, conversation_id, message_id):
    message = get_object_or_404(Message, pk=message_id)
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    newthought = Thought()
    newthought.text = request.POST['newthought' + str(message_id)]
    newthought.datetime = request.POST['thoughtdate' + str(message_id)]
    newthought.message = message

    newthought.save()

    return render(request, 'conversational/detail.html', {'conversation': conversation})


def addconversation(request):
    try:
        conversation = Conversation()
        conversation.title = request.POST['title']
        conversation.datetime = request.POST['date']
    except (KeyError, Conversation.DoesNotExist):
        return render(request, 'conversational/detail.html', {
            'conversation': conversation,
            'error_message': "Something went wrong.",
        })
    else:
        conversation.save()

        return HttpResponseRedirect(reverse('index'))


def searchconversationtitles(request):
    searchterm = request.POST['searchterm']
    queryset = Conversation.objects.filter(title__icontains=searchterm)
    context = {
        'queryset': queryset,
    }
    template = loader.get_template('conversational/conversationsearch.html')
    return HttpResponse(template.render(context, request))


def searchmessagetext(request):
    searchterm = request.POST['messagesearchterm']
    queryset = Message.objects.filter(text__icontains=searchterm)
    context = {
        'queryset': queryset,
    }
    template = loader.get_template('conversational/messagesearch.html')
    return HttpResponse(template.render(context, request))
