import datetime
from google.cloud.firestore_v1 import ArrayUnion, ArrayRemove

from ..config import authe, db

from .utils import get_res_public_id


def create_account(email, passw, full_name, trofi_code):
    # Setup initial user account
    try:
        user = authe.create_user_with_email_and_password(email, passw)

        uid = user['localId']

        res_ref = db.collection(u'restaurants').document(
            "trofi-res-" + trofi_code)

        res_private_ref = res_ref.collection(u'private').document(uid)

        logs_ref = res_ref.collection(u'logs')

        foods_ref = db.collection(u'foods').where(
            u'restaurant_id', u'==', trofi_code)

        batch = db.batch()

        food_data = foods_ref.get()
        menu = []
        for food in food_data:
            try:
                menu.append(food.id)
                single_food_ref = db.collection(u'foods').document(food.id)
                single_food_private_ref = db.collection(
                    u'foods').document(food.id).collection(u'private')
                private_docs = single_food_private_ref.get()
                for doc in private_docs:
                    old_food_private_ref = single_food_private_ref.document(
                        doc.id)
                    private_food_data = doc.to_dict()

                new_food_private_ref = single_food_private_ref.document(uid)
                batch.set(new_food_private_ref,
                          private_food_data)
                old_food_private_ref.delete()
                batch.update(single_food_ref, {
                    "restaurant_id": "trofi-res-" + trofi_code})
            except Exception as e:
                return None, e

        batch.set(res_ref, {
            "is_active": True,
            "name": "",
            "logo": "",
            "opening_hour": 0,
            "closing_hour": 0,
            "menu": menu,
            "tags": [],
            "desc": "",
            "address": "",
            "contact_email": "",
            "contact_phone": "",
        })

        now = datetime.datetime.now()

        batch.set(res_private_ref, {
            "accepted_code": trofi_code,
            "user_name": full_name,
            "allow_in": True,
            "payment_id": "",
            "total_orders": 0,
            "credit_card_percentage": 0,
            "credit_card_constant": 0,
            "joined": now,
            "last_login": now,
        })

        batch.set(logs_ref.document("00-00-0000"), {
            "discounts": [],
        })

        general_ref = db.collection(u'general').document("trofi-verification")
        batch.update(
            general_ref, {u'accepted_codes_unused': ArrayRemove([trofi_code])})
        batch.update(
            general_ref, {u'accepted_codes_used': ArrayUnion([trofi_code])})

        map_ref = db.collection(u'general').document(
            "trofi-verification").collection(uid).document("map")
        batch.set(map_ref, {
            "public_id": "trofi-res-" + trofi_code,
        })

        # Commit the batch
        batch.commit()
    except Exception as e:
        return None, e

    print("Restaurant successfully written!")
    return user, None


def log_in(email, passw):
    # Log the user in
    try:
        user = authe.sign_in_with_email_and_password(email, passw)

        uid = user['localId']
        public_id, e = get_res_public_id(uid)

        if public_id is None:
            return None, e, None, None

        now = datetime.datetime.now()
        res_private_ref = db.collection(u'restaurants').document(
            public_id).collection(u'private').document(uid)
        res_private_ref.update({u'last_login': now})

    except Exception as e:
        return None, e, None, None
    return user, None, uid, public_id
