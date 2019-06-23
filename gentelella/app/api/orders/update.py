from ..common import api_success, api_db_error


def update_food_status_ready(db, uid, body):
    order_id = body["order_id"]
    order_ref = db.collection(u'orders').document("wbc_transc_" + order_id)

    if body["order_ready"] == True:
        try:
            order_ref.update({u'status_ready': True})
        except Exception as e:
            return api_db_error(e)
    else:
        try:
            order_ref.update({u'status_ready': False})
        except Exception as e:
            return api_db_error(e)

    return api_success()
