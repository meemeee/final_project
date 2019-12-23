from django_private_chat.models import Dialog
from django.db.models import Q

def new_message_alert(request_user):
    convos = Dialog.objects.filter(Q(owner=request_user) | Q(opponent=request_user))
    for convo in convos:
        # Check if the latest messages sent by others are unread by this user
        if not convo.messages.last().read and convo.messages.last().sender != request_user:
            return True