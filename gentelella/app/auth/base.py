import datetime
from google.cloud.firestore_v1 import ArrayUnion, ArrayRemove

from ..config import authe, db

from .utils import get_res_public_id


def create_account(email, passw, full_name, trofi_code):
    # Setup initial user account
    try:
        user = authe.create_user_with_email_and_password(email, passw)

        uid = user['localId']

        res_ref = db.collection(u'restaurants').document("trofi-res-" + trofi_code)

        res_private_ref = res_ref.collection(u'private').document(uid)

        more_info_ref = res_ref.collection(u'more-info').document(u'details')
        logs_ref = res_ref.collection(u'logs')

        batch = db.batch()

        batch.set(res_ref, {
            "all_discounts_active": False,
            "restaurant_name": "",
            "restaurant_logo": "",
            "op_hours": "00-00",
            "menu": [],
            "tags": [],
            })

        now = datetime.datetime.now()

        batch.set(res_private_ref, {
            "accepted_code": trofi_code,
            "name": full_name,
            "allow_in": False,
            "payment_id": "",
            "total_orders": 0,
            "credit_card_percentage": 0,
            "credit_card_constant": 0,
            "orders": [],
            "joined": now,
            "last_login": now,
            })

        batch.set(more_info_ref, {
            "restaurant_desc": "",
            "address": "",
            "contact_email": "",
            "contact_phone": "",
            })

        batch.set(logs_ref.document("00-00-0000"), {
            "discounts": [],
            })

        general_ref = db.collection(u'general').document("trofi-verification")
        batch.update(general_ref, {u'accepted_codes_unused': ArrayRemove([trofi_code])})
        batch.update(general_ref, {u'accepted_codes_used': ArrayUnion([trofi_code])})

        map_ref = db.collection(u'general').document("trofi-verification").collection(uid).document("map")
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
        res_private_ref = db.collection(u'restaurants').document(public_id).collection(u'private').document(uid)
        res_private_ref.update({u'last_login': now})

    except Exception as e:
        return None, e, None, None
    return user, None, uid, public_id
