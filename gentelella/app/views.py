from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

import pyrebase
import json
import datetime


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from google.cloud.firestore_v1 import ArrayUnion, ArrayRemove


config = {
  "apiKey": "AIzaSyCwgogOI0rJDijj-r97dbWjEinKkrBH1Ok",
  "authDomain": "daydesign-a277f.firebaseapp.com",
  "databaseURL": "https://daydesign-a277f.firebaseio.com",
  "storageBucket": "daydesign-a277f.appspot.com"
}

firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
authe = firebase.auth()

# firestore config
# Use a service account
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def time_display(time_24):
    from datetime import datetime
    return datetime.strptime(time_24, "%H:%M").strftime("%I:%M %p")

@csrf_exempt
def api_hours(request, hour_id = -1):
    # TODO: ADD AUTHENTICATION
    # TODO: implement, public_id = request.session['public_uid']
    uid = request.session['admin_uid']

    # GET
    # TODO: RETURN ALL HOURS DATA

    if request.method == "GET":
        if hour_id == -1:
            response = {
            "message": "Returning all hours..."
            }
            return JsonResponse(response) 

    # PUT
    if request.method == "PUT":
        body = json.loads(str(request.body, encoding='utf-8'))
        # print(body)
        if body["id"] == "food-status-active":
            hour_id = body["hour_id"]
            food_id = body["food_id"]
            hour_ref = db.collection(u'restaurants').document(uid).collection(u'hours').document(hour_id)

            if body["food_active"] == True:
                try:
                    hour_ref.update({u'foods_active': ArrayUnion([food_id])})                            
                except Exception as e:
                    print(e)                    
            else:            
                try:
                    hour_ref.update({u'foods_active': ArrayRemove([food_id])})
                except Exception as e:
                    print(e) 
        elif body["id"] == "hour-status-active":
            hour_id = body["hour_id"]            
            hour_ref = db.collection(u'restaurants').document(uid).collection(u'hours').document(hour_id)

            if body["hour_active"] == True:
                try:
                    hour_ref.update({u'hour_is_active': True})                         
                except Exception as e:
                    print(e)                    
            else:            
                try:
                    hour_ref.update({u'hour_is_active': False})
                except Exception as e:
                    print(e) 
        elif body["id"] == "percent-discount-update":
            hour_id = body["hour_id"]        
            new_discount = body["starting_discount"]            
            hour_ref = db.collection(u'restaurants').document(uid).collection(u'hours').document(hour_id)  
 
            try:
                hour_data = hour_ref.get().to_dict()
                print()
                # print(hour_data.discounts[0])                
                initial_discount = {
                    "is_active": hour_data["discounts"][0]["is_active"],
                    "needed_contribution": 0,
                    "percent_discount": new_discount,
                }      
                print(initial_discount) 
                try:
                    hour_ref.update({u'discounts': ArrayRemove([hour_data["discounts"][0]])})    
                    hour_ref.update({u'discounts': ArrayUnion([initial_discount])})         
                except Exception as e:
                    print(e) 
                
            except Exception as e:
                print(u'No such document!')
    
    response = {
        "message": "Success!"
    }
    return JsonResponse(response) 

@csrf_exempt
def api_orders(request, order_id = -1):
    # TODO: ADD AUTHENTICATION
    # TODO: implement, public_id = request.session['public_uid']
    uid = request.session['admin_uid']

    # GET
    if request.method == "GET":
        if order_id == -1:
            response = {
            "message": "Returning all orders..."
            }
            return JsonResponse(response) 

    if request.method == "PUT":
        body = json.loads(str(request.body, encoding='utf-8'))
        # print(body)

        if body["id"] == "food-status-ready":
            order_id = body["order_id"]
            order_ref = db.collection(u'orders').document("wbc_transc_" + order_id)

            if body["order_ready"] == True:
                try:
                    order_ref.update({u'status_ready': True})                       
                except Exception as e:
                    print(e)                    
            else:            
                try:
                    order_ref.update({u'status_ready': False})
                except Exception as e:
                    print(e) 

    response = {
        "message": "Success!"
    }
    return JsonResponse(response)

def logout(request):
    auth.logout(request)
    response = redirect('signIn')
    return response

def signUp(request):
    if logged_in(request):
        response = redirect('incoming')
        return response  

    email = request.POST.get("email")
    passw = request.POST.get("password")
    fname = request.POST.get("fname")
    trofi_code = request.POST.get("trofi_code")

    if not email and not passw and not fname and not trofi_code:
        context = {}
        template = loader.get_template('app/signup.html')
        return HttpResponse(template.render(context, request))

    # Check if valid trofi code
    codeRef = db.collection(u'general').document(u'trofi-verification')

    try:
        doc = codeRef.get()
        # print(u'Document data: {}'.format(doc.to_dict()))
        if trofi_code in doc.to_dict()["accepted_codes"]:            
            # Sign the user up
            try:
                user = authe.create_user_with_email_and_password(email, passw)
                ## TODO: create user entry in database and auto setup
            except Exception as e:
                error_json = e.args[1]        
                error = json.loads(error_json)['error']        
                message=error['message']
                context = {"messg":message, "email": email, "passw": passw, "fname": fname, "trofi_code": trofi_code}
                # response = redirect('signIn',context=context)
                # return response
                template = loader.get_template('app/signup.html')        
                return HttpResponse(template.render(context, request))

            # print(user)
            # print("debug")
            session_id=user['idToken']
            request.session['uid']=str(session_id)
            response = redirect('incoming')
            return response
        else:
            message="Invalid Trofi Code!"
            context = {"messg":message, "email": email, "passw": passw, "fname": fname, "trofi_code": trofi_code}
            template = loader.get_template('app/signup.html')        
            return HttpResponse(template.render(context, request))
    except Exception as e:
        # print(u'No such document!')
        message="Problem with database. Contact software.wbc@gmail.com"
        context = {"messg":message, "email": email, "passw": passw, "fname": fname, "trofi_code": trofi_code}
        template = loader.get_template('app/signup.html')        
        return HttpResponse(template.render(context, request))

def signIn(request):
    if logged_in(request):
        response = redirect('incoming')
        return response   

    email = request.POST.get("email")
    passw = request.POST.get("password")

    if not email or not passw:
        context = {}
        template = loader.get_template('app/login.html')
        return HttpResponse(template.render(context, request))

    # Log the user in
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except Exception as e:
        error_json = e.args[1]        
        error = json.loads(error_json)['error']        
        message=error['message']
        context = {"messg":message, "email": email, "passw": passw}
        # response = redirect('signIn',context=context)
        # return response
        template = loader.get_template('app/login.html')        
        return HttpResponse(template.render(context, request))

    # print(user['localId'])
    uid = user['localId']
    resRef = db.collection(u'restaurants').document(uid)
    resPrivateRef = resRef.collection(u'private').document(uid)

    try:
        doc = resPrivateRef.get()
        data = doc.to_dict()
        # print(u'Document data: {}'.format(doc.to_dict()))
        if data["allow_in"]:
                session_id=user['idToken']
                request.session['uid']=str(session_id)
                request.session['admin_uid']=str(uid)
                request.session['uname']=data["name"]
                request.session['ccf_percentage']=data["credit_card_percentage"]
                request.session['ccf_constant']=data["credit_card_constant"]
                response = redirect('incoming')
                return response
        else:
            message="Vibe has not setup your account yet. Please wait to receive an email."
            context = {"messg":message, "email": email, "passw": passw}
            template = loader.get_template('app/login.html')        
            return HttpResponse(template.render(context, request))

    except Exception as e:
        # print(u'No such document!')
        message="Problem with database. Contact software.wbc@gmail.com"
        context = {"messg":message, "email": email, "passw": passw}
        template = loader.get_template('app/login.html')        
        return HttpResponse(template.render(context, request))

def lost(request):
    if logged_in(request):
        response = redirect('incoming')
        return response 
    else:
        response = redirect('signIn')
        return response 

def logged_in(request):
    try:
        return request.session['uid']
    except KeyError:
        return None

def incoming(request):
    if not logged_in(request):
        response = redirect('signIn')
        return response 
    # print(request.session['uid'])
    uid = request.session['admin_uid']
    uname = request.session['uname']

    # load data
    incoming_orders_data = []

    # Create a callback on_snapshot function to capture changes
    def on_orders_count_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            # print(u'Received document data: {}'.format(doc.to_dict()))
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
                    pass
            
            print("render")
            print(incoming_orders_data)
            # context = {"incoming_orders": incoming_orders_data}
            # template = loader.get_template('app/incoming.html')
            # return HttpResponse(template.render(context, request))

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

    context = {"incoming_orders": incoming_orders_data, "name": uname}
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
    context = {"all_orders": all_orders_data, "name": uname}
    template = loader.get_template('app/history.html')
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

