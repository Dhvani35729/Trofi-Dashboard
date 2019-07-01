from ..common import api_success, api_db_error
# import threading
# from threading import Timer


# def updateCurrentOrderStatus(order_ref):
#     # print("I'm running on thread %s" % threading.current_thread())
#     order_ref.update(
#         {'current_order': False})


def update_food_status_ready(db, uid, body):
    order_id = body["order_id"]
    order_ref = db.collection(u'orders').where(
        "order_number", u"==", order_id).get()

    for order in order_ref:
        # print(u'{} => {}'.format(res.id, res.to_dict()))
        order_ref = db.collection(u'orders').document(order.id)
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
