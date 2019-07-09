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
from .foods.update import (
    update_food_sales_price,
    update_food_profit_margin,
    update_food_ingredients_cost,
)
from .restaurants.get import (
    get_all_restaurants_with_hours,
    get_all_restaurants_with_hour,
)
from .restaurants.restaurant.get import (
    get_restaurant_with_hours,
    get_restaurant_with_hour,
    get_restaurant_with_menu,
    get_restaurant_with_menu_for_hour,
)
from .users.get import (
    get_user_orders,
    get_user_current_order,
    get_user_default_card,
    get_user_cards,
    get_auth,
)
from .users.post import (
    post_user_order,
    post_user_add_card,
    post_user_change_default_card
)
from .other.get import get_app_maint
from .other.update import (
    update_ccf_percentage,
    update_ccf_constant,
)

# TODO: Check out django_rest_framework
# TODO: Catch proper firebase exceptions
from django.views.decorators.csrf import ensure_csrf_cookie


def api_app_maint(request):
    if request.method == "GET":
        return get_app_maint(db)
    else:
        return error_500(request, None)


def api_auth(request, user_private_id):
    if request.method == "GET":
        return get_auth(db, user_private_id)
    if request.method == "POST":
        return error_500(request, None)


@csrf_exempt
def api_user_add_card(request, user_private_id):
    if request.method == "GET":
        return error_500(request, None)
    if request.method == "POST":
        body = json.loads(str(request.body, encoding='utf-8'))
        return post_user_add_card(db, user_private_id, body)


@csrf_exempt
def api_user_cards(request, user_private_id):
    if request.method == "GET":
        return get_user_cards(db, user_private_id)


def api_user_card_default(request, user_private_id):
    if request.method == "GET":
        return get_user_default_card(db, user_private_id)
    elif request.method == "POST":
        body = json.loads(str(request.body, encoding='utf-8'))
        return post_user_change_default_card(db, user_private_id, body)


@csrf_exempt
def api_user_order_new(request, user_private_id):
    if request.method == "GET":
        return error_500(request, None)
    elif request.method == "POST":
        body = json.loads(str(request.body, encoding='utf-8'))
        return post_user_order(db, user_private_id, body)


def api_user_all_orders(request, user_private_id):
    if request.method == "GET":
        return get_user_orders(db, user_private_id)


def api_user_current_order(request, user_private_id):
    if request.method == "GET":
        return get_user_current_order(db, user_private_id)


def api_restaurants_hour(request, hour_id=-1):
    if request.method == "GET":
        if hour_id == -1:
            return get_all_restaurants_with_hours(db)
        else:
            return get_all_restaurants_with_hour(db, hour_id)


def api_restaurant_hour(request, restaurant_id, hour_id=-1):
    if request.method == "GET":
        if hour_id == -1:
            return get_restaurant_with_hours(db, restaurant_id)
        else:
            return get_restaurant_with_hour(db, restaurant_id, hour_id)


def api_restaurant_menu(request, restaurant_id, hour_id=-1):
    if request.method == "GET":
        if hour_id == -1:
            return get_restaurant_with_menu(db, restaurant_id)
        else:
            return get_restaurant_with_menu_for_hour(db, restaurant_id, hour_id)

# TODO: add CSRF support
@csrf_exempt
def api_hours(request, hour_id=-1):
    # TODO: ADD AUTHENTICATION
    try:
        uid = request.session['admin_uid']
        public_id = request.session['public_id']
    except Exception as e:
        return error_500(request, e)

    # PUT
    if request.method == "PUT":
        body = json.loads(str(request.body, encoding='utf-8'))

        if body["id"] == "food-status-active":
            return update_food_status_active(db, public_id, uid, body)
        elif body["id"] == "hour-status-active":
            return update_hour_status(db, public_id, uid, body)
        elif body["id"] == "percent-discount-update":
            return update_percent_discount(db, public_id, uid, body)
        elif body["id"] == "payroll-update":
            return update_payroll(db, public_id, uid, body)
        elif body["id"] == "overhead-cost-update":
            return update_overhead_cost(db, public_id, uid, body)

    return error_500(request, None)

# TODO: add CSRF support
@csrf_exempt
def api_orders(request, order_id=-1):
    # TODO: ADD AUTHENTICATION
    try:
        uid = request.session['admin_uid']
        # public_id = request.session['public_id']
    except Exception as e:
        return error_500(request, e)

    # TODO: Support GET

    if request.method == "PUT":
        body = json.loads(str(request.body, encoding='utf-8'))

        if body["id"] == "food-status-ready":
            return update_food_status_ready(db, uid, body)

    return error_500(request, None)

# TODO: add CSRF support
@csrf_exempt
def api_foods(request, food_id=-1):
    # TODO: ADD AUTHENTICATION
    try:
        uid = request.session['admin_uid']
        # public_id = request.session['public_id']
    except Exception as e:
        return error_500(request, e)

    # TODO: Support GET

    if request.method == "PUT":
        body = json.loads(str(request.body, encoding='utf-8'))

        if body["id"] == "sales-price-update":
            return update_food_sales_price(db, uid, body)
        elif body["id"] == "profit-margin-update":
            return update_food_profit_margin(db, uid, body)
        elif body["id"] == "ingredients-cost-update":
            return update_food_ingredients_cost(db, uid, body)

    return error_500(request, None)

# TODO: add CSRF support
@csrf_exempt
def api_others(request):
    # TODO: ADD AUTHENTICATION
    try:
        uid = request.session['admin_uid']
        public_id = request.session['public_id']
    except Exception as e:
        return error_500(request, e)

    if request.method == "PUT":
        body = json.loads(str(request.body, encoding='utf-8'))

        if body["id"] == "ccf-percentage-update":
            return update_ccf_percentage(db, public_id, uid, body)
        elif body["id"] == "ccf-constant-update":
            return update_ccf_constant(db, public_id, uid, body)

    return error_500(request, None)
