from Admin.fcm import send_push_notification

def notify_user(user, product, old_price, new_price):
    title = f"Narx o'zgardi 🔔"
    body = f"{product.title}: {old_price} → {new_price}"

    send_push_notification(
        token=user.onesignal_player_id,
        title=title,
        body=body,
        data={
            "type": "price_change",
            "product_id": str(product.id)
        }
    )
