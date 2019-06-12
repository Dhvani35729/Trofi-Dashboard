from django.http import JsonResponse
from firebase_admin import auth


def user_not_found(user_id):
    return JsonResponse({
        "error": {
            "code": "UserNotFound",
            "id": user_id,
            "message": "The specified user does not exist",
        }
    })


def order_not_found(user_id):
    return JsonResponse({
        "error": {
            "code": "CurrentOrderNotFound",
            "id": user_id,
            "message": "No current orders found for the specified user",
        }
    })


def get_user_orders(db, user_private_id):

    try:
        auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    order_data = db.collection(u'orders').where(
        u'user', u'==', user_private_id).get()

    all_orders = []

    for order in order_data:
        order_data = order.to_dict()

        order = {
            "res_name": order_data["restaurant_name"],
            "order_number": order_data["order_id"],
            "status": order_data["status_ready"],
            "pickup_time":  order_data["hour_end"],
            "foods": order_data["foods"],
        }

        all_orders.append(order)

    return JsonResponse({"list": all_orders})


def get_user_current_order(db, user_private_id):

    try:
        auth.get_user(user_private_id)
    except:
        return user_not_found(user_private_id)

    order_data = db.collection(u'orders').where(
        u'user', u'==', user_private_id).where(
        u'status_ready', u'==', False).get()

    for order in order_data:
        order_data = order.to_dict()

        order = {
            "res_name": order_data["restaurant_name"],
            "order_number": order_data["order_id"],
            "status": order_data["status_ready"],
            "pickup_time":  order_data["hour_end"],
            "foods": order_data["foods"],
        }

        return JsonResponse(order)

    return order_not_found(user_private_id)
