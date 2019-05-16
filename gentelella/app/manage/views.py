from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse

from ..auth.utils import logged_in
from ..constants import HOME_PAGE_LOGGED_OUT
from ..utils import time_display, error_500
from ..config import db


def manage(request):
    if not logged_in(request):
        response = redirect(HOME_PAGE_LOGGED_OUT)
        return response
    
    # TODO: implement: public_id = request.session['public_uid']
    uid = request.session['admin_uid']
    uname = request.session['uname']

    template_name = 'app/manage.html'

    other = {
        "ccf_percentage": request.session['ccf_percentage'],
        "ccf_constant": request.session['ccf_constant'],
    }

    # load data
    res_ref = db.collection(u'restaurants').document(uid)

    # hours and menu
    hours_data = []
    menu = []

    try:
        res_public_data = res_ref.get().to_dict()
        hours_ref = res_ref.collection("hours")
        open_hours = res_public_data["op_hours"]
        opening = int(open_hours[0:2])
        closing = int(open_hours[3:5])

        for food in res_public_data["menu"]:
            food_ref = db.collection(u'foods').document(food)
            try:
                food_public_data = food_ref.get().to_dict()
                food_private_ref = food_ref.collection("private").document(uid)

                try:
                    food_private_data = food_private_ref.get().to_dict()
                    food_item = {
                        "id": food,
                        "name": food_public_data["name"],
                        "sales_price": food_public_data["sales_price"],
                        "ingredients_cost": food_private_data["ingredients_cost"],
                        "profit_margin": food_private_data["profit_margin"]
                    }

                    menu.append(food_item)
                except Exception as e:
                    # TODO: add error message to show to user
                    return error_500(request)

            except Exception as e:
                # TODO: add error message to show to user
                return error_500(request)

        hours_query = hours_ref.where("start_id", ">=", opening).where("start_id", "<", closing)
        hours_docs = hours_query.get()
        for hour in hours_docs:
            all_hours_data = hour.to_dict()
            starting_discount = 0
            for discount in all_hours_data["discounts"]:
                if discount["is_active"]:
                    starting_discount = discount["percent_discount"]
                    break

            display_id = ""
            if int(hour.id) < 10:
                display_id = time_display("0" + hour.id + ":00")
            else:
                display_id = time_display(hour.id + ":00")

            an_hour = {
                "sort_id": int(hour.id),
                "display_id":  display_id,
                "starting_discount": starting_discount,
                "active": all_hours_data["hour_is_active"],
                "foods_active": all_hours_data["foods_active"],
                # "overhead_costs": all_hours_data["overhead_cost"],
                # "payroll": all_hours_data["payroll"],
            }

            hours_data.append(an_hour)

    except Exception as e:
        # TODO: add error message to show to user
        return error_500(request)

    context = {"hours_data": hours_data, "menu": menu, "other": other, "name": uname}
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request))
