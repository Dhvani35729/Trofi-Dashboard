from django.http import JsonResponse
from ...constants import DISCOUNT_INCREMENT


def get_all_restaurants_with_hours(db, active=True):
    res_ref = db.collection(u'restaurants').where(
        u'all_discounts_active', u'==', True).get()

    all_hours = {}

    for i in range(24):
        all_hours[i] = {"key": int(i), "data": []}

    for res in res_ref:
        # print(u'{} => {}'.format(res.id, res.to_dict()))
        res_public_data = res.to_dict()

        hours_ref = db.collection(u'restaurants').document(res.id).collection(
            u'hours').where(u'start_id', u'>=', res_public_data["opening_hour"]).where(u'start_id', u'<=', res_public_data["closing_hour"])

        if active:
            hours_ref = hours_ref.where(u'hour_is_active', u'==', True)

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
                    current_discount = float(discount)
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
                "key": res.id,
                "name": res_public_data["restaurant_name"],
                "tags": res_public_data["tags"],
                "needed_contribution": hour_data["needed_contribution"],
                "current_discount": current_discount,
                "next_discount": next_discount,
                "max_discount_reached": max_discount_reached,
                "current_contribution": current_contribution,
            }
            all_hours[hour_id]["data"].append(res_card)

    return JsonResponse(all_hours)


def get_all_restaurants_with_hour(db, hour_id, active=True):
    res_ref = db.collection(u'restaurants').where(
        u'all_discounts_active', u'==', True).get()

    all_hours = {"key": str(hour_id), "data": []}

    for res in res_ref:
        # print(u'{} => {}'.format(res.id, res.to_dict()))
        res_public_data = res.to_dict()

        hours_ref = db.collection(u'restaurants').document(res.id).collection(
            u'hours').where(u'start_id', u'==', int(hour_id))

        if active:
            hours_ref = hours_ref.where(u'hour_is_active', u'==', True)

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
                    current_discount = float(discount)
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
                "key": res.id,
                "name": res_public_data["restaurant_name"],
                "tags": res_public_data["tags"],
                "needed_contribution": hour_data["needed_contribution"],
                "current_discount": current_discount,
                "next_discount": next_discount,
                "max_discount_reached": max_discount_reached,
                "current_contribution": current_contribution,
            }
            all_hours["data"].append(res_card)

    return JsonResponse(all_hours)
