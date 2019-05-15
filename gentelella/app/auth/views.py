
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib import auth

from ..utils import (
    error_message,
    get_message_from_exception,
    )

from ..constants import HOME_PAGE, HOME_PAGE_LOGGED_OUT, DATABASE_ERROR_MSG

from .base import (
    create_account,
    log_in,
    )

from .utils import (
    logged_in,
    is_valid_trofi_code,
    should_allow_user_in
    )


def logout(request):
    auth.logout(request)
    response = redirect(HOME_PAGE_LOGGED_OUT)
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
        message = DATABASE_ERROR_MSG
        context = {"messg": message, "email": email, "passw": passw, "fname": fname, "trofi_code": trofi_code}
        return error_message(request, message, context, template_name)            

    if not is_valid:
        message = "Invalid Trofi Code!"
        context = {"messg": message, "email": email, "passw": passw, "fname": fname, "trofi_code": trofi_code}
        return error_message(request, message, context, template_name)
    else:
        user, e = create_account(email, passw)
        if user:
            response = redirect('logout')
            return response
        else:  
            message = get_message_from_exception(e)
            context = {"messg": message, "email": email, "passw": passw, "fname": fname, "trofi_code": trofi_code}
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
            context = {"messg": message, "email": email, "passw": passw}
            return error_message(request, message, context, template_name)
        
        if allow_user_in:
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            request.session['admin_uid'] = str(uid)
            request.session['uname'] = data["name"]
            request.session['ccf_percentage'] = data["credit_card_percentage"]
            request.session['ccf_constant'] = data["credit_card_constant"]
            response = redirect(HOME_PAGE)
            return response

        else:
            message = "Vibe has not setup your account yet. Please wait to receive an email."
            context = {"messg": message, "email": email, "passw": passw}
            return error_message(request, message, context, template_name)
    else:      
        message = get_message_from_exception(e)
        context = {"messg": message, "email": email, "passw": passw}
        return error_message(request, message, context, template_name)