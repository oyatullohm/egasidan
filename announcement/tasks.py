from announcement.models import Product, PriceWatch
from celery import shared_task
from decimal import Decimal
# from .utils import notify_user
from main.models import UserFollow
from Admin.fcm import send_bulk_push

# @shared_task(
#     bind=True,
#     autoretry_for=(Exception,),
#     retry_backoff=5,
#     retry_kwargs={'max_retries': 3}
# )
# def send_price_notifications(self, product_id, old_price, new_price):

#     product = Product.objects.only('id', 'title').get(id=product_id)

#     watchers = list(
#         PriceWatch.objects
#         .filter(product_id=product_id)
#         .select_related('user')
#     )

#     if not watchers:
#         return "No watchers"

#     updated = []

#     for watch in watchers:
#         user = watch.user

#         if not user.fcm_token:
#             continue

#         notify_user(
#             user=user,
#             product=product,
#             old_price=old_price,
#             new_price=new_price
#         )

#         watch.last_price = Decimal(new_price)
#         updated.append(watch)

#     if updated:
#         PriceWatch.objects.bulk_update(updated, ['last_price'])

#     return f"Notified {len(updated)} users"


# @shared_task(
#     bind=True,
#     autoretry_for=(Exception,),
#     retry_backoff=5,
#     retry_kwargs={'max_retries': 3}
# )
# def notify_followers_new_product(self,product_id):
#     """
#     Product yaratilganda obunachilarga push yuboradi
#     """
#     product = Product.objects.select_related('user').get(id=product_id)
#     user = product.user

#     followers = (
#         UserFollow.objects
#         .filter(following=user)
#         .select_related('follower')
#     )

#     tokens = [
#         f.follower.onesignal_player_id
#         for f in followers
#         if f.follower.onesignal_player_id
#     ]

#     if not tokens:
#         return "No followers"

#     send_bulk_push(
#         tokens=tokens,
#         title="Yangi e'lon 🔥",
#         body=f"{user.username} yangi mahsulot joyladi: {product.title}",
#         data={
#             "type": "new_product",
#             "product_id": str(product.id)
#         }
#     )

#     return f"Sent to {len(tokens)} users"
