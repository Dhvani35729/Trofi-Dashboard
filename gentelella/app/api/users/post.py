from django.http import JsonResponse
from firebase_admin import auth, firestore
import stripe
import datetime
import uuid
from app.constants import DISCOUNT_INCREMENT

stripe.api_key = "sk_test_WZJim1CVcSc7WBSKjdRDxJGS"


def user_not_found(user_id):
    return JsonResponse({
        "error": {
            "code": "UserNotFound",
            "id": user_id,
            "message": "The specified user does not exist",
        }
    })


def user_card_added(user_id):
    return JsonResponse({
        "success": {
            "code": "CardAdded",
            "id": user_id,
            "message": "Succesfully added a card for the specified user",
        }
    })


def user_card_not_added(user_id):
    return JsonResponse({
        "error": {
            "code": "CardNotAdded",
            "id": user_id,
            "message": "Could not add the card for the specified user",
        }
    })


def user_card_changed(user_id):
    return JsonResponse({
        "success": {
            "code": "CardChanged",
            "id": user_id,
            "message": "Succesfully changed a card for the specified user",
        }
    })


def user_card_not_changed(user_id):
    return JsonResponse({
        "error": {
            "code": "CardNotChanged",
            "id": user_id,
            "message": "Could not change the card for the specified user",
        }
    })


def post_user_change_default_card(db, user_private_id, body):
    try:
        user = auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    user_public_id = 'trofi-user-6'

    # CHECK IF USER HAS ID
    user_private_ref = db.collection(u'users').document(
        user_public_id).collection(u'private').document(user_private_id)

    user_private_data = user_private_ref.get().to_dict()
    import pdb
    pdb.set_trace()
    if user_private_data["stripe_id"] == "":
        return user_not_found(user_private_id)
    else:
        try:
            stripe.Customer.modify(
                user_private_data["stripe_id"],
                default_source=body["cardId"]
            )
            user_private_ref.update(
                {u'default_card': body["last4"]})
            return user_card_changed(user_private_id)
        except:
            return user_card_not_changed(user_private_id)


def post_user_add_card(db, user_private_id, body):
    try:
        user = auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    user_public_id = 'trofi-user-6'

    # CHECK IF USER HAS ID
    user_private_ref = db.collection(u'users').document(
        user_public_id).collection(u'private').document(user_private_id)

    user_private_data = user_private_ref.get().to_dict()
    import pdb
    pdb.set_trace()
    if user_private_data["stripe_id"] == "":
        stripe_user = stripe.Customer.create(
            email=user.email,
        )
        card = stripe.Customer.create_source(
            stripe_user.id,
            source=body["tokenId"]
        )
        user_private_ref.update(
            {u'stripe_id': stripe_user.id, u'default_card': card.last4})
        return user_card_added(user_private_id)
    else:
        try:
            card = stripe.Customer.create_source(
                user_private_data["stripe_id"],
                source=body["tokenId"]
            )
            return user_card_added(user_private_id)
        except:
            return user_card_not_added(user_private_id)


def post_user_order(db, user_private_id, body):
    try:
        user = auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    user_public_id = 'trofi-user-6'

    # CHECK IF USER HAS ID
    user_private_ref = db.collection(u'users').document(
        user_public_id).collection(u'private').document(user_private_id)

    user_private_data = user_private_ref.get().to_dict()
    import pdb
    pdb.set_trace()
    try:
        # Use Stripe's library to make requests...
        if user_private_data["stripe_id"] == "":
            return user_not_found(user_private_id)
        else:
            # using default card
            if body["card"] == "default":
                charge = stripe.Charge.create(
                    amount=body['order']['initial_total'],
                    currency="cad",
                    customer=user_private_data["stripe_id"],
                    capture=False,
                )
            else:
                # SHOW ERROR
                return
    except:
        # STRIPE ERROR
        return

    try:
        now = datetime.datetime.now()
        body['order']["charge_id"] = charge.id
        body['order']["card_id"] = charge.payment_method
        body['order']["last4"] = charge.payment_method_details.card.last4
        body['order']["placed_at"] = now

        initial_total_contribution = 0.0
        for food in body['order']["foods"]:
            initial_total_contribution += food["initial_contribution"] * \
                food["quantity"]

        body['order']["initial_total_contribution"] = initial_total_contribution
    except:
        # SERVER ERROR
        return

    try:
        orders_ref = db.collection(u'orders').document()
        body['order']["order_number"] = orders_ref.id[-7:]
        orders_ref.set(body['order'])
    except:
        # FIREBASE ERROR
        return

    # update contribution and change discount if neccessary

    hours_ref = db.collection(u'restaurants').document(
        body['order']["restaurant_id"]).collection(u'hours').document(str(body["order"]["hour_id"]))

    # GET CURRENT DISCOUNT

    hour_data = hours_ref.get().to_dict()

    current_discount = 0

    new_all_discounts = hour_data["discounts"]
    all_contributions = hour_data["contributions"]
    max_discount = hour_data["max_discount"]
    max_discount_reached = False
    # pdb.set_trace()
    for discount in sorted(new_all_discounts):
        if new_all_discounts[discount]["is_active"] is True:
            current_discount = float(discount.replace('_', '.'))
            if max_discount == current_discount:
                max_discount_reached = True
        if max_discount != float(discount.replace('_', '.')):
            for food in body["order"]["foods"]:
                new_all_discounts[discount]["current_contributed"] += all_contributions[food["id"]
                                                                                        ][discount] * food["quantity"]
    # pdb.set_trace()
    if max_discount_reached:
        return

    for discount in sorted(new_all_discounts):
        if new_all_discounts[discount]["is_active"] is True:
            if new_all_discounts[discount]["current_contributed"] >= hour_data["needed_contribution"]:
                new_all_discounts[discount]["is_active"] = False
                next_discount = float(discount.replace(
                    '_', '.')) + DISCOUNT_INCREMENT
                next_discount = "{0:.2f}".format(
                    next_discount).replace('.', '_')
                new_all_discounts[next_discount]["is_active"] = True

    hours_ref.update({
        "discounts": new_all_discounts
    })

    return JsonResponse({"success": "success"})
