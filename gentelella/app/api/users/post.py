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
        # TODO: Check if order_number already exists
        body['order']["order_number"] = str(uuid.uuid4())[:7]
        body['order']["placed_at"] = now
    except:
        # SERVER ERROR
        return

    try:
        orders_ref = db.collection(u'orders')
        orders_ref.document(
            "wbc_transc_" + body['order']["order_number"]).set(body['order'])
    except:
        # FIREBASE ERROR
        return

    # update contribution and change discount if neccessary

    hours_ref = db.collection(u'restaurants').document(
        body['order']["restaurant_id"]).collection(u'hours').document(str(body["order"]["hour_id"]))

    # GET CURRENT DISCOUNT

    hour_data = hours_ref.get().to_dict()

    current_discount = 0
    next_discount = 0
    current_contribution = 0

    all_discounts = hour_data["discounts"]
    max_discount = hour_data["max_discount"]
    max_discount_reached = False
    for discount in sorted(all_discounts):
        if all_discounts[discount]["is_active"] is True:
            current_discount = float(discount)
            current_contribution = all_discounts[discount]["current_contributed"]
            if max_discount != current_discount:
                next_discount = current_discount + DISCOUNT_INCREMENT
            else:
                max_discount_reached = True
                next_discount = max_discount
            break

    if max_discount_reached:
        return

    initial_total_contribution = 0.0
    for food in body['order']["foods"]:
        initial_total_contribution += food["initial_contribution"] * \
            food["quantity"]

    body['order']["initial_total_contribution"] = initial_total_contribution

    new_contribution = current_contribution + \
        body['order']["initial_total_contribution"]

    current_discount = "{0:.2f}".format(current_discount)
    current_discount = current_discount.replace('.', '\.')

    pdb.set_trace()
    if new_contribution == hour_data["needed_contribution"]:
        hours_ref.update({
            "discounts." + current_discount + ".current_contributed": new_contribution,
            "discounts." + current_discount + ".is_active": False,
            "discounts." + next_discount + ".is_active": True,
            # figure out what to multiply it by
            "discounts." + next_discount + ".current_contributed": new_contribution * DISCOUNT_INCREMENT,
        })
    else:
        hours_ref.update({
            "discounts." + current_discount + ".current_contributed": new_contribution
        })

    return JsonResponse({"success": "success"})
