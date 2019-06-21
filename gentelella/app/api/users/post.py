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


def post_user_order(db, user_private_id, order):
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
            if order["card"] == "default":
                charge = stripe.Charge.create(
                    amount=order['order']['amount']['total'],
                    currency="cad",
                    customer=user_private_data["stripe_id"],
                    capture=False,
                )
            else:
                # SHOW ERROR
                pass
    except:
        # STRIPE ERROR
        return

    # trofi work

    return JsonResponse({"success": "success"})
