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


def get_user_cards(db, user_private_id):
    try:
        user = auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    user_public_id = 'trofi-user-6'

    # CHECK IF USER HAS ID
    user_private_ref = db.collection(u'users').document(
        user_public_id).collection(u'private').document(user_private_id).get()

    user_private_data = user_private_ref.to_dict()

    if user_private_data["stripe_id"] != "":
        all_cards = stripe.PaymentMethod.list(
            customer=user_private_data["stripe_id"], type="card")
    else:
        # RETURN NO CARDS FOUND
        pass


def post_user_order(db, user_private_id, order):
    try:
        user = auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)
    try:
        # Use Stripe's library to make requests...

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
                source=order["tokenId"]
            )
            response = stripe.Charge.create(
                amount=order["amount"],
                currency="cad",
                customer=stripe_user.id,
                source=card.id,
                description="Order #: ok"
            )

            user_private_ref.update(
                {u'stripe_id': stripe_user.id, u'default_card': card.last4})
        else:
            # using default card
            if order["card"] == "default":
                response = stripe.Charge.create(
                    amount=order["amount"],
                    currency="cad",
                    customer=user_private_data["stripe_id"],
                    description="Order #: ok"
                )
            else:
                import pdb
                pdb.set_trace()
                stripe_user = stripe.Customer.retrieve(
                    user_private_data["stripe_id"])
                card = stripe.Customer.create_source(
                    stripe_user.id,
                    source=order["tokenId"]
                )
                response = stripe.Charge.create(
                    amount=order["amount"],
                    currency="cad",
                    customer=stripe_user.id,
                    source=card.id,
                    description="Order #: ok"
                )

        return JsonResponse(response)
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err = body.get('error', {})

        print("Status is: %s" % e.http_status)
        print("Type is: %s" % err.get('type'))
        print("Code is: %s" % err.get('code'))
        # param is '' in this case
        print("Param is: %s" % err.get('param'))
        print("Message is: %s" % err.get('message'))
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        pass
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        pass
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        pass
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        pass
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        pass


# post_user_order(db, 'UHrIUw19XLWV2amsKm7u5weEadZ2', {"ok": "hi"})
