from ..utils import get_user_public_id
from django.http import JsonResponse
from firebase_admin import auth
import stripe

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

        return JsonResponse(order_data)

    return order_not_found(user_private_id)
