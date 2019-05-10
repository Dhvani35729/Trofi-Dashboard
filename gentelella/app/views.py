from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib import auth
import pyrebase
import json
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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

def status(request, order_id, checked):
    if not logged_in(request):
        response = redirect('signIn')
        return response  

    order_ref = db.collection(u'orders').document("wbc_transc_" + order_id)

    if checked == 0:
        order_ref.update({u'status_ready': False})
    else:
        order_ref.update({u'status_ready': True})

    # print(order_id)
    response = redirect('incoming')
    return response

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
            pass

    # Watch the document
    # orders_count_watch = orders_count_ref.on_snapshot(on_orders_count_snapshot)

    context = {"incoming_orders": incoming_orders_data, "name": uname}
    print('render outside')
    print(context)
    template = loader.get_template('app/incoming.html')
    return HttpResponse(template.render(context, request))

def manage(request):
    context = {}
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

