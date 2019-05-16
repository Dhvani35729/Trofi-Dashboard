from django.template import loader
from django.http import HttpResponse
from django.template.response import TemplateResponse

import json


# convert 24 hour time string to 12 hour time string
def time_display(time_24):
    from datetime import datetime
    return datetime.strptime(time_24, "%H:%M").strftime("%I:%M %p")


def money_display(money_decimal):
    precision = 2
    return "{:.{}f}".format(money_decimal, precision)


def error_message(request, message, context, template_name):
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request))


def get_message_from_exception(e):
    error_json = e.args[1]
    error = json.loads(error_json)['error']
    return error['message']


def error_500(request):
    return TemplateResponse(request, "app/page_500.html", status=500)