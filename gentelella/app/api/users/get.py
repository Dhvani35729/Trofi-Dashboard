from ..utils import get_user_public_id
from django.http import JsonResponse
from firebase_admin import auth
import stripe
import datetime
from google.cloud.firestore_v1 import Increment
from ..restaurants.restaurant.get import get_restaurant_with_hour
import json

stripe.api_key = "sk_test_WZJim1CVcSc7WBSKjdRDxJGS"


def user_not_found(user_id):
    return JsonResponse({
        "error": {
            "code": "UserNotFound",
            "id": user_id,
            "message": "The specified user does not exist",
        }
    })


def order_not_found(user_id):
    return JsonResponse({
        "error": {
            "code": "CurrentOrderNotFound",
            "id": user_id,
            "message": "No current orders found for the specified user",
        }
    })


def default_card_not_found(user_id):
    return JsonResponse({
        "error": {
            "code": "DefaultCardNotFound",
            "id": user_id,
            "message": "No default card found for the specified user",
        }
    })


def cards_not_found(user_id):
    return JsonResponse({
        "error": {
            "code": "CardsNotFound",
            "id": user_id,
            "message": "No cards found for the specified user",
        }
    })


def general_error():
    return JsonResponse({
        "error": {
            "code": "GeneralError",
            "message": "A problem occurred...",
        }
    })


def get_auth(db, user_private_id):
    try:
        user = auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    user_public_id = get_user_public_id(user_private_id)

    now = datetime.datetime.now()

    if user_public_id:
        user_private_ref = db.collection(u'users').document(
            user_public_id).collection(u'private').document(user_private_id)
        user_private_ref.update({
            "num_opened": Increment(1),
            "last_opened": now
        })
        return JsonResponse({"success": {"user_public_id": user_public_id}})
    else:
        # new user
        try:
            user_ref = db.collection(u'users').document()
            public_id = user_ref.id
            user_private_ref = user_ref.collection(
                u'private').document(user_private_id)
            batch = db.batch()

            batch.set(user_ref, {"name": user.display_name, "friends": []})
            batch.set(user_private_ref, {
                "avg_time": 0.0,
                "num_opened": 1,
                "date_joined": now,
                "last_opened": now,
                "default_card": -1,
                "stripe_id": ""
            })
            user_map_ref = db.collection(u'general').document(
                u'user-verification').collection(user_private_id).document(u'map')
            batch.set(user_map_ref, {"public_id": public_id})

            general_ref = db.collection('general').document('maint')
            batch.update(general_ref, {"total_users": Increment(1)})

            batch.commit()
            return JsonResponse({"success": {"user_public_id": public_id}})
        except:
            return general_error()

    pass


def get_user_cards(db, user_private_id):
    try:
        auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    user_public_id = get_user_public_id(user_private_id)

    user_private_ref = db.collection(u'users').document(
        user_public_id).collection(u'private').document(user_private_id).get()

    user_private_data = user_private_ref.to_dict()

    if user_private_data["stripe_id"] != '':
        stripe_user = stripe.Customer.retrieve(user_private_data["stripe_id"])
        cards = []
        for card in stripe_user.sources.data:
            formatted_card = {
                "id": card.id,
                "brand": card.brand,
                "last4": card.last4,
                "funding": card.funding,
                "default": stripe_user.default_source == card.id
            }
            cards.append(formatted_card)
        if len(cards) == 0:
            return cards_not_found(user_private_id)

        return JsonResponse({"list": cards})
    else:
        return cards_not_found(user_private_id)


def get_user_default_card(db, user_private_id):
    try:
        auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    user_public_id = get_user_public_id(user_private_id)

    user_private_ref = db.collection(u'users').document(
        user_public_id).collection(u'private').document(user_private_id).get()

    user_private_data = user_private_ref.to_dict()

    if user_private_data["default_card"] != -1:
        return JsonResponse({"last4": user_private_data["default_card"]})
    else:
        return default_card_not_found(user_private_id)


def get_user_orders(db, user_private_id):
    try:
        auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    order_data = db.collection(u'orders').where(
        u'user', u'==', user_private_id).get()

    all_orders = []

    for order in order_data:
        order_data = order.to_dict()

        all_orders.append(order_data)

    return JsonResponse({"list": all_orders})


def get_user_current_order(db, user_private_id):

    try:
        auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    order_data = db.collection(u'orders').where(
        u'user', u'==', user_private_id).where(
        u'current_order', u'==', True).get()

    for order in order_data:
        order_data = order.to_dict()
        hour_response = get_restaurant_with_hour(
            db, order_data["restaurant_id"], str(order_data["hour_id"]))
        hour_data = json.loads(hour_response.content)

        return JsonResponse({"order_info": order_data, "hour_info": hour_data})

    return order_not_found(user_private_id)
