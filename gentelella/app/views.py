from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib import auth

import json
import datetime

from .utils import (
    time_display,
    error_message,
    get_message_from_exception,
    )
from .config import authe, db
from .api.base import api_hours, api_orders
from .constants import HOME_PAGE, DATABASE_ERROR_MSG

from .auth.base import (    
    create_account,    
    log_in,
    )

from .auth.utils import (
    logged_in,
    is_valid_trofi_code,
    should_allow_user_in
    )

def index(request):
    if logged_in(request):
        response = redirect(HOME_PAGE)
    else:
        response = redirect('signIn')
    return response

def logout(request):
    auth.logout(request)
    response = redirect('signIn')
    return response

def sign_up(request):
    if logged_in(request):
        response = redirect(HOME_PAGE)
        return response  

    template_name = 'app/signup.html' 

    email = request.POST.get("email")
    passw = request.POST.get("password")
    fname = request.POST.get("fname")
    trofi_code = request.POST.get("trofi_code")

    if not email and not passw and not fname and not trofi_code:
        context = {}
        template = loader.get_template('app/signup.html')
        return HttpResponse(template.render(context, request))

    # Check if valid trofi code
    is_valid = is_valid_trofi_code(trofi_code)

    if is_valid is None:
        message=DATABASE_ERROR_MSG
        context = {"messg":message, "email": email, "passw": passw, "fname": fname, "trofi_code": trofi_code}                   
        return error_message(request, message, context, template_name)            

    if not is_valid:
        message="Invalid Trofi Code!"
        context = {"messg":message, "email": email, "passw": passw, "fname": fname, "trofi_code": trofi_code}        
        return error_message(request, message, context, template_name)
    else:
        user, e = create_account(email, passw)
        if user:
            response = redirect('logout')
            return response
        else:  
            message = get_message_from_exception(e)
            context = {"messg":message, "email": email, "passw": passw, "fname": fname, "trofi_code": trofi_code}
            return error_message(request, message, context, template_name)      


def sign_in(request):
    if logged_in(request):
        response = redirect(HOME_PAGE)
        return response   

    template_name = 'app/login.html' 

    email = request.POST.get("email")
    passw = request.POST.get("password")

    if not email or not passw:
        context = {}
        template = loader.get_template('app/login.html')
        return HttpResponse(template.render(context, request))

    user, e = log_in(email, passw)
    if user:        
        uid = user['localId']

        allow_user_in, data = should_allow_user_in(uid)
        
        if allow_user_in is None:
            message = DATABASE_ERROR_MSG
            context = {"messg":message, "email": email, "passw": passw}               
            return error_message(request, message, context, template_name)
        
        if allow_user_in:
            session_id=user['idToken']
            request.session['uid']=str(session_id)
            request.session['admin_uid']=str(uid)
            request.session['uname']=data["name"]
            request.session['ccf_percentage']=data["credit_card_percentage"]
            request.session['ccf_constant']=data["credit_card_constant"]
            response = redirect(HOME_PAGE)
            return response

        else:
            message="Vibe has not setup your account yet. Please wait to receive an email."
            context = {"messg":message, "email": email, "passw": passw}               
            return error_message(request, message, context, template_name)
    else:      
        message = get_message_from_exception(e)
        context = {"messg":message, "email": email, "passw": passw}             
        return error_message(request, message, context, template_name)

def incoming(request):
    if not logged_in(request):
        response = redirect('signIn')
        return response 
    # print(request.session['uid'])
    uid = request.session['admin_uid']
    uname = request.session['uname']

    # load data
    incoming_orders_data = []

    orders_count_ref = db.collection(u'restaurants').document(uid).collection(u'private').document(uid)

    # Order Number, Order Placed At, Order Active Between, Current Price, Items, Toppings, Comments, Status
    all_orders_ref = db.collection(u'restaurants').document(uid).collection(u'private').document(uid).collection("orders")
    all_incoming_orders_query = all_orders_ref.where(u'incoming', u'==', True)
    all_incoming_orders_docs = all_incoming_orders_query.get()
    #incoming_orders_data.clear()
    for doc in all_incoming_orders_docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))   
        incoming_order_ref = db.collection(u'orders').document(doc.id)
        try:
            incoming_order = incoming_order_ref.get()
            order_data = incoming_order.to_dict()
            # print(u'Document data: {}'.format(order_data))                       
            order_hours = order_data["placed_at"] - datetime.timedelta(hours=4)                                        
            placed_at = str(order_hours.time())[:5]
            active_hours = order_data["hours_order"][0:2] + ":00" + " - " + order_data["hours_order"][3:5] + ":00"
            
            an_order = {
                "id": order_data["order_id"],
                "placed_at": placed_at,
                "active_between": active_hours,
                "current_price": order_data["total_price"],
                "items": order_data["foods"],
                "status": order_data["status_ready"],
            }

            incoming_orders_data.append(an_order)                    
        except Exception as e:
            # TODO: add error message to show to user
            print(e)
            pass

    # Watch the document
    # orders_count_watch = orders_count_ref.on_snapshot(on_orders_count_snapshot)

    context = {"incoming_orders": incoming_orders_data,"admin_uid": uid, "name": uname}
    print('render outside')
    print(context)
    template = loader.get_template('app/incoming.html')
    return HttpResponse(template.render(context, request))

def manage(request):
    if not logged_in(request):
        response = redirect('signIn')
        return response 
    # print(request.session['uid'])
    # TODO: implement, public_id = request.session['public_uid']
    uid = request.session['admin_uid']
    uname = request.session['uname']

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
        hours_ref = db.collection(u'restaurants').document(uid).collection("hours")
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
                    "cost_ingredients": food_private_data["cost_ingredients"],
                    "profit_margin": food_private_data["profit_margin"]
                    }                                        

                    menu.append(food_item)
                except Exception as e:
                    # TODO: add error message to show to user
                    print('here')
                    print(e)
                    pass    

            except Exception as e:
                # TODO: add error message to show to user
                print('here')
                print(e)
                pass


        hours_query = hours_ref.where("start_id", ">=", opening).where("start_id", "<", closing)
        hours_docs = hours_query.get()
        for hour in hours_docs:
            # print(u'{} => {}'.format(hour.id, hour.to_dict()))   
            all_hours_data = hour.to_dict()
            starting_discount = 0
            for discount in all_hours_data["discounts"]:
                if discount["is_active"]:
                    starting_discount = discount["percent_discount"]
                    break 

            # TODO: Convert to 24 hour
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
        print('here')
        print(e)
        pass
    

    context = {"hours_data": hours_data, "menu": menu, "other": other, "name": uname}
    template = loader.get_template('app/manage.html')
    return HttpResponse(template.render(context, request))

def history(request):
    if not logged_in(request):
        response = redirect('signIn')
        return response 

    # print(request.session['uid'])
    uid = request.session['admin_uid']
    uname = request.session['uname']

    # load data
    all_orders_data = []

    # Order Number, Order Placed At, Order Active Between, Current Price, Items, Toppings, Comments, Status
    all_orders_ref = db.collection(u'restaurants').document(uid).collection(u'private').document(uid).collection("orders")
        
    all_orders_docs = all_orders_ref.get()
    #incoming_orders_data.clear()
    for doc in all_orders_docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))   
        order_ref = db.collection(u'orders').document(doc.id)
        try:
            order = order_ref.get()
            order_data = order.to_dict()
            # print(u'Document data: {}'.format(order_data))                       
            active_hours = order_data["hours_order"][0:2] + ":00" + " - " + order_data["hours_order"][3:5] + ":00"
            
            an_order = {
                "id": order_data["order_id"],                
                "active_between": active_hours,
                "final_price": float(order_data["total_price"]) * (100.0 - order_data["final_discount"])/100.0,
                "items": order_data["foods"],                
            }

            all_orders_data.append(an_order)                    
        except Exception as e:
            # TODO: add error message to show to user
            pass

    # Watch the document
    # orders_count_watch = orders_count_ref.on_snapshot(on_orders_count_snapshot)
    print(all_orders_data)
    context = {"all_orders": all_orders_data, "admin_uid": uid, "name": uname}
    template = loader.get_template('app/history.html')
    return HttpResponse(template.render(context, request))


