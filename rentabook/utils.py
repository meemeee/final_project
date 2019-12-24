from django_private_chat.models import Dialog
from django.db.models import Q

def new_message_alert(request_user):
    convos = Dialog.objects.filter(Q(owner=request_user) | Q(opponent=request_user))
    if len(convos) > 0:
        for convo in convos:
            if convo.messages.all().count() > 0:
                # Check if the latest messages sent by others are unread by this user
                if not convo.messages.last().read and convo.messages.last().sender != request_user:
                    return True
    return False


def get_messaged_users(request_user):
    dialogs = Dialog.objects.filter(Q(owner=request_user) | Q(opponent=request_user))
    messaged_users = list()
    for dialog in dialogs:
        if dialog.owner == request_user:
            messaged_users.append(dialog.opponent)
        else:
            messaged_users.append(dialog.owner)

    return messaged_users
