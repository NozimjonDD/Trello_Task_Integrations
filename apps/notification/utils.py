from firebase_admin import messaging


def send_push_notification(fcm_token, title, body, data):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data,
        token=fcm_token,
    )

    response = messaging.send(message)

    print('Successfully sent message:', response)
