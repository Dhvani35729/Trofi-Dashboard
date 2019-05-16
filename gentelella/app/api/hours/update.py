from google.cloud.firestore_v1 import ArrayUnion, ArrayRemove

from ..common import api_success, api_db_error


def update_food_status_active(db, uid, body):
    hour_id = body["hour_id"]
    food_id = body["food_id"]
    hour_ref = db.collection(u'restaurants').document(uid).collection(u'hours').document(hour_id)

    if body["food_active"] == True:
        try:
            hour_ref.update({u'foods_active': ArrayUnion([food_id])})
        except Exception as e:
            return api_db_error(e)
    else:
        try:
            hour_ref.update({u'foods_active': ArrayRemove([food_id])})
        except Exception as e:
            return api_db_error(e)

    return api_success()


def update_hour_status(db, uid, body):
    hour_id = body["hour_id"]
    hour_ref = db.collection(u'restaurants').document(uid).collection(u'hours').document(hour_id)

    if body["hour_active"] == True:
        try:
            hour_ref.update({u'hour_is_active': True})
        except Exception as e:
            return api_db_error(e)
    else:
        try:
            hour_ref.update({u'hour_is_active': False})
        except Exception as e:
            return api_db_error(e)

    return api_success()


def update_percent_discount(db, uid, body):
    hour_id = body["hour_id"]
    new_discount = body["starting_discount"]
    hour_ref = db.collection(u'restaurants').document(uid).collection(u'hours').document(hour_id)

    try:
        hour_data = hour_ref.get().to_dict()
        initial_discount = {
            "is_active": hour_data["discounts"][0]["is_active"],
            "needed_contribution": 0,
            "percent_discount": new_discount,
        }

        #TODO: Check for edge cases
        try:
            hour_ref.update({u'discounts': ArrayRemove([hour_data["discounts"][0]])})
            hour_ref.update({u'discounts': ArrayUnion([initial_discount])})
        except Exception as e:
            return api_db_error(e)
    except Exception as e:
        return api_db_error(e)

    return api_success()


def update_payroll(db, uid, body):
    hour_id = body["hour_id"]
    new_payroll = body["payroll"]
    hour_ref = db.collection(u'restaurants').document(uid).collection(u'hours').document(hour_id)

    try:
        hour_ref.update({u'payroll': float(new_payroll)})
    except Exception as e:
        return api_db_error(e)

    return api_success()


def update_overhead_cost(db, uid, body):
    hour_id = body["hour_id"]
    new_operating = body["overhead_cost"]
    hour_ref = db.collection(u'restaurants').document(uid).collection(u'hours').document(hour_id)

    try:
        hour_ref.update({u'overhead_cost': float(new_operating)})
    except Exception as e:
        return api_db_error(e)

    return api_success()
