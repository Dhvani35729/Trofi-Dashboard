from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse

from ..auth.utils import logged_in
from ..constants import HOME_PAGE_LOGGED_OUT
from ..utils import money_display, time_display, error_500
from ..config import db


def history(request):
    if not logged_in(request):
        response = redirect(HOME_PAGE_LOGGED_OUT)
        return response

    # print(request.session['uid'])
    uid = request.session['admin_uid']
    public_id = request.session['public_id']
    uname = request.session['uname']

    template_name = 'app/history.html'

    # load data
    all_orders_data = []

    # Order Number, Order Placed At, Order Active Between, Current Price, Items, Toppings, Comments, Status
    all_orders_ref = db.collection(u'restaurants').document(public_id).collection(u'private').document(uid).collection("orders")

    all_orders_docs = all_orders_ref.get()

    for order in all_orders_docs:
        order_ref = db.collection(u'orders').document(order.id)
        try:
            order_data = order_ref.get().to_dict()

            active_hours = time_display(order_data["hours_order"][0:2] + ":00") + " - " + time_display(order_data["hours_order"][3:5] + ":00")

            an_order = {
                "id": order_data["order_id"],
                "active_between": active_hours,
                "final_price": money_display(order_data["total_price"] * (100.0 - order_data["final_discount"])/100.0),
                "items": order_data["foods"],
            }

            all_orders_data.append(an_order)
        except Exception as e:
            # TODO: add error message to show to user
            return error_500(request, e)

    context = {"all_orders": all_orders_data, "public_id": public_id, "admin_uid": uid, "name": uname}
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request))
