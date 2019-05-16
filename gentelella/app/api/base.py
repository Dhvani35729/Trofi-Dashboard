from django.views.decorators.csrf import csrf_exempt

import json

from ..config import db
from ..utils import error_500

from .hours.update import (
    update_food_status_active,
    update_hour_status,
    update_percent_discount,
    update_payroll,
    update_overhead_cost
    )
from .orders.update import (
    update_food_status_ready,
    )

# TODO: Check out django_rest_framework
# TODO: Catch proper firebase exceptions

# TODO: add CSRF support
@csrf_exempt
def api_hours(request, hour_id = -1):
    # TODO: ADD AUTHENTICATION
    # TODO: implement: public_id = request.session['public_uid']
    try:
        uid = request.session['admin_uid']
    except KeyError:
        return error_500(request)

    # TODO: Support GET

    # PUT
    if request.method == "PUT":
        body = json.loads(str(request.body, encoding='utf-8'))
        
        if body["id"] == "food-status-active":            
            return update_food_status_active(db, uid, body)
        elif body["id"] == "hour-status-active":
            return update_hour_status(db, uid, body)
        elif body["id"] == "percent-discount-update":
            return update_percent_discount(db, uid, body)
        elif body["id"] == "payroll-update":
            return update_payroll(db, uid, body)
        elif body["id"] == "overhead-cost-update":
            return update_overhead_cost(db, uid, body)
    
    return error_500(request) 

# TODO: add CSRF support
@csrf_exempt
def api_orders(request, order_id = -1):
    # TODO: ADD AUTHENTICATION
    # TODO: implement: public_id = request.session['public_uid']
    try:
        uid = request.session['admin_uid']
    except KeyError:
        return error_500(request)

    # TODO: Support GET

    if request.method == "PUT":
        body = json.loads(str(request.body, encoding='utf-8'))
        # print(body)

        if body["id"] == "food-status-ready":
            return update_food_status_ready(db, uid, body)

    return error_500(request)