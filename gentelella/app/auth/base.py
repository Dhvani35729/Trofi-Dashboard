import datetime
from google.cloud.firestore_v1 import ArrayUnion, ArrayRemove

from ..config import authe, db

from .utils import get_res_public_id


def create_account(email, passw, full_name, trofi_code):
    # Setup initial user account
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        # TODO: create user entry in database and auto setup
        # TODO: Show loading
        uid = user['localId']

        res_ref = db.collection(u'restaurants').document("trofi-res-" + trofi_code)

        res_private_ref = res_ref.collection(u'private').document(uid)

        more_info_ref = res_ref.collection(u'more-info').document(u'details')
        logs_ref = res_ref.collection(u'logs')

        init_hours_ref = res_ref.collection(u'hours')

        init_0_hours_ref = init_hours_ref.document("0")
        init_1_hours_ref = init_hours_ref.document("1")
        init_2_hours_ref = init_hours_ref.document("2")
        init_3_hours_ref = init_hours_ref.document("3")
        init_4_hours_ref = init_hours_ref.document("4")
        init_5_hours_ref = init_hours_ref.document("5")
        init_6_hours_ref = init_hours_ref.document("6")
        init_7_hours_ref = init_hours_ref.document("7")
        init_8_hours_ref = init_hours_ref.document("8")
        init_9_hours_ref = init_hours_ref.document("9")
        init_10_hours_ref = init_hours_ref.document("10")
        init_11_hours_ref = init_hours_ref.document("11")
        init_12_hours_ref = init_hours_ref.document("12")
        init_13_hours_ref = init_hours_ref.document("13")
        init_14_hours_ref = init_hours_ref.document("14")
        init_15_hours_ref = init_hours_ref.document("15")
        init_16_hours_ref = init_hours_ref.document("16")
        init_17_hours_ref = init_hours_ref.document("17")
        init_18_hours_ref = init_hours_ref.document("18")
        init_19_hours_ref = init_hours_ref.document("19")
        init_20_hours_ref = init_hours_ref.document("20")
        init_21_hours_ref = init_hours_ref.document("21")
        init_22_hours_ref = init_hours_ref.document("22")
        init_23_hours_ref = init_hours_ref.document("23")

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

        batch.set(init_0_hours_ref, {
            "start_id": 0,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_1_hours_ref, {
            "start_id": 1,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_2_hours_ref, {
            "start_id": 2,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_3_hours_ref, {
            "start_id": 3,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_4_hours_ref, {
            "start_id": 4,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_5_hours_ref, {
            "start_id": 5,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_6_hours_ref, {
            "start_id": 6,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_7_hours_ref, {
            "start_id": 7,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_8_hours_ref, {
            "start_id": 8,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_9_hours_ref, {
            "start_id": 9,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_10_hours_ref, {
            "start_id": 10,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_11_hours_ref, {
            "start_id": 11,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_12_hours_ref, {
            "start_id": 12,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_13_hours_ref, {
            "start_id": 13,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_14_hours_ref, {
            "start_id": 14,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_15_hours_ref, {
            "start_id": 15,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_16_hours_ref, {
            "start_id": 16,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_17_hours_ref, {
            "start_id": 17,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_18_hours_ref, {
            "start_id": 18,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_19_hours_ref, {
            "start_id": 19,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_20_hours_ref, {
            "start_id": 20,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_21_hours_ref, {
            "start_id": 21,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_22_hours_ref, {
            "start_id": 22,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
            })
        batch.set(init_23_hours_ref, {
            "start_id": 23,
            "payroll": 0,
            "overhead_cost": 0,
            "current_contributed": 0,
            "hour_is_active": False,
            "initial_discount": 0,
            "discounts": [],
            "foods_active": []
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
