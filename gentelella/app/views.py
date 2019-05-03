from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib import auth
import pyrebase
import json

config = {
  "apiKey": "AIzaSyCwgogOI0rJDijj-r97dbWjEinKkrBH1Ok",
  "authDomain": "daydesign-a277f.firebaseapp.com",
  "databaseURL": "https://daydesign-a277f.firebaseio.com",
  "storageBucket": "daydesign-a277f.appspot.com"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
authe = firebase.auth()

def logout(request):
    auth.logout(request)
    response = redirect('signIn')
    return response

def signUp(request):
    try:
        request.session['uid']
        response = redirect('index')
        return response   
    except KeyError:
        pass

    email = request.POST.get("email")
    passw = request.POST.get("password")
    fname = request.POST.get("fname")
    trofi_code = request.POST.get("trofi_code")

    if not email and not passw and not fname and not trofi_code:
        context = {}
        template = loader.get_template('app/signup.html')
        return HttpResponse(template.render(context, request))

    



    # Sign the user up
    try:
        user = authe.create_user_with_email_and_password(email, passw)
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
    response = redirect('index')
    return response

def signIn(request):
    try:
        request.session['uid']
        response = redirect('index')
        return response   
    except KeyError:
        pass

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

    # print(user)
    # print("debug")
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    response = redirect('index')
    return response

def index(request):
    try:
        request.session['uid']
    except KeyError:
        response = redirect('signIn')
        return response   
    print(request.session['uid'])

    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))

def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

