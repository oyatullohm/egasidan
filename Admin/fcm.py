# Admin/fcm.py
from firebase_admin import messaging

def send_push_notification(token, title, body, data=None):
    if not token:
        return "No token"

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        token=token,
    )

    response = messaging.send(message)
    return response


def send_bulk_push(tokens, title, body, data=None):
    if not tokens:
        return "No tokens"

    messages = []

    for token in tokens:
        messages.append(
            messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                token=token,
            )
        )

    response = messaging.send_all(messages)
    return response
