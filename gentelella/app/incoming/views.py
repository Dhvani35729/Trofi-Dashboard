from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse

import datetime

from ..auth.utils import logged_in
from ..constants import HOME_PAGE_LOGGED_OUT
from ..utils import money_display, time_display, error_500
from ..config import db


def incoming(request):
    if not logged_in(request):
        response = redirect(HOME_PAGE_LOGGED_OUT)
        return response

    # print(request.session['uid'])
    uid = request.session['admin_uid']
    public_id = request.session['public_id']
    uname = request.session['uname']

    template_name = 'app/incoming.html'

    # load data
    incoming_orders_data = []

    # Order Number, Order Placed At, Order Active Between, Current Price, Items, Toppings, Comments, Status
    all_orders_ref = db.collection(u'orders').where(
        u'restaurant_id', u'==', public_id)
    all_incoming_orders_query = all_orders_ref.where(
        u'status_ready', u'==', False)
    all_incoming_orders_docs = all_incoming_orders_query.get()

    for order in all_incoming_orders_docs:
        try:
            order_data = order.to_dict()

            order_hours = order_data["placed_at"] - datetime.timedelta(hours=4)

            placed_at = time_display(str(order_hours.time())[:5])
            active_hours = time_display(
                str(order_data["hour_start"]) + ":00") + " - " + time_display(str(order_data["hour_end"]) + ":00")

            an_order = {
                "id": order_data["order_number"],
                "placed_at": placed_at,
                "active_between": active_hours,
                "current_price": order_data["initial_total"] / 100,
                "items": order_data["foods"],
                "status": order_data["status_ready"],
            }

            incoming_orders_data.append(an_order)
        except Exception as e:
            # TODO: add error message to show to user
            return error_500(request, e)

    context = {"incoming_orders": incoming_orders_data,
               "public_id": public_id, "admin_uid": uid, "name": uname}
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request))
