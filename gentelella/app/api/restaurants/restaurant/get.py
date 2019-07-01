from django.http import JsonResponse
from app.constants import DISCOUNT_INCREMENT


def restaurant_not_found(res_public_id):
    return JsonResponse({
        "error": {
            "code": "RestaurantNotFound",
            "id": res_public_id,
            "message": "The specified restaurant does not exist",
        }
    })


def get_restaurant_with_menu(db, res_public_id):
    res_hour_ref = db.collection(u'restaurants').document(
        res_public_id).get()

    res_public_data = res_hour_ref.to_dict()

    if res_public_data is None:
        return restaurant_not_found(res_public_id)

    menu = []

    for food_id in res_public_data["menu"]:
        food_ref = db.collection(u'foods').document(food_id).get()
        food_data = food_ref.to_dict()

        toppings_data = []
        for topping in food_data["toppings"]:
            toppings_data.append({
                "key": topping
            })

        food = {
            "key": food_id,
            "name": food_data["name"],
            "desc": food_data["desc"],
            "original_price": food_data["sales_price"],
            "toppings": toppings_data
        }

        menu.append(food)

    return JsonResponse({"list": menu})


def get_restaurant_with_menu_for_hour(db, res_public_id, hour_id, active=True):
    res_hour_ref = db.collection(u'restaurants').document(
        res_public_id).collection(u'hours').document(hour_id).get()

    res_hour_data = res_hour_ref.to_dict()

    if res_hour_data is None:
        return restaurant_not_found(res_public_id)

    menu = []

    for food_id in res_hour_data["foods_active"]:
        food_ref = db.collection(u'foods').document(food_id).get()
        food_data = food_ref.to_dict()

        current_discount = "0.00"
        all_discounts = res_hour_data["discounts"]
        max_discount = res_hour_data["max_discount"]
        for discount in sorted(all_discounts):
            if all_discounts[discount]["is_active"] is True:
                current_discount = discount
        if float(current_discount.replace("_", ".")) == max_discount:
            current_contribution = 0
        else:
            current_contribution = res_hour_data["contributions"][food_id][current_discount]

        toppings_data = []
        for topping in food_data["toppings"]:
            toppings_data.append({
                "key": topping
            })

        food = {
            "key": food_id,
            "name": food_data["name"],
            "desc": food_data["desc"],
            "original_price": food_data["sales_price"],
            "tags": food_data["tags"],
            "toppings": toppings_data,
            "contribution": current_contribution,
        }

        menu.append(food)

    return JsonResponse({"list": menu})


def get_restaurant_with_hours(db, res_public_id, active=True):
    res_data = db.collection(u'restaurants').document(res_public_id).get()

    all_hours = []

    for i in range(24):
        all_hours.append({"key": str(i), "data": []})

    # print(u'{} => {}'.format(res.id, res.to_dict()))
    res_public_data = res_data.to_dict()

    if res_public_data is None:
        return restaurant_not_found(res_public_id)

    hours_ref = db.collection(u'restaurants').document(res_data.id).collection(
        u'hours').where(u'start_id', u'>=', res_public_data["opening_hour"]).where(u'start_id', u'<=', res_public_data["closing_hour"])

    if active:
        hours_ref = hours_ref.where(u'is_active', u'==', True)

    hours_ref = hours_ref.get()
    for hour in hours_ref:
        # print(u'{} => {}'.format(hour.id, hour.to_dict()))
        hour_data = hour.to_dict()

        current_discount = 0
        next_discount = 0
        current_contribution = 0

        all_discounts = hour_data["discounts"]
        max_discount = hour_data["max_discount"]
        max_discount_reached = False
        for discount in sorted(all_discounts):
            if all_discounts[discount]["is_active"] is True:
                current_discount = float(discount.replace("_", "."))
                current_contribution = all_discounts[discount]["current_contributed"]
                if max_discount != current_discount:
                    next_discount = current_discount + DISCOUNT_INCREMENT
                else:
                    max_discount_reached = True
                    next_discount = max_discount
                break

        hour_id = int(hour_data["start_id"])
        res_card = {
            "hour_id": hour_id,
            "key": res_data.id,
            "name": res_public_data["name"],
            "tags": res_public_data["tags"],
            "needed_contribution": hour_data["needed_contribution"],
            "max_discount_reached": max_discount_reached,
            "current_discount": current_discount,
            "next_discount": next_discount,
            "current_contribution": current_contribution,
        }
        all_hours[hour_id]["data"].append(res_card)

    return JsonResponse({"list": all_hours})


def get_restaurant_with_hour(db, res_public_id, hour_id, active=True):
    res_data = db.collection(u'restaurants').document(res_public_id).get()

    all_hours = {"key": str(hour_id), "data": []}

    # print(u'{} => {}'.format(res.id, res.to_dict()))
    res_public_data = res_data.to_dict()

    if res_public_data is None:
        return restaurant_not_found(res_public_id)

    hours_ref = db.collection(u'restaurants').document(res_data.id).collection(
        u'hours').where(u'start_id', u'==', int(hour_id))

    if active:
        hours_ref = hours_ref.where(u'is_active', u'==', True)

    hours_ref = hours_ref.get()
    for hour in hours_ref:
        # print(u'{} => {}'.format(hour.id, hour.to_dict()))
        hour_data = hour.to_dict()

        current_discount = 0
        next_discount = 0
        current_contribution = 0

        all_discounts = hour_data["discounts"]
        max_discount = hour_data["max_discount"]
        max_discount_reached = False
        for discount in sorted(all_discounts):
            if all_discounts[discount]["is_active"] is True:
                current_discount = float(discount.replace("_", "."))
                current_contribution = all_discounts[discount]["current_contributed"]
                if max_discount != current_discount:
                    next_discount = current_discount + DISCOUNT_INCREMENT
                else:
                    max_discount_reached = True
                    next_discount = max_discount
                break

        hour_id = int(hour_data["start_id"])
        res_card = {
            "hour_id": hour_id,
            "key": res_data.id,
            "name": res_public_data["name"],
            "tags": res_public_data["tags"],
            "needed_contribution": hour_data["needed_contribution"],
            "max_discount_reached": max_discount_reached,
            "current_discount": current_discount,
            "next_discount": next_discount,
            "current_contribution": current_contribution,
        }
        all_hours["data"].append(res_card)

    return JsonResponse(all_hours)
