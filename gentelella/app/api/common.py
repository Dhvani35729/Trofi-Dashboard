from django.http import JsonResponse
from django.template.response import TemplateResponse

def api_success():
    response = {
        "status": 200,
        "message": "Success!"
    }
    return JsonResponse(response) 

def api_error(request):
    return TemplateResponse(request, "app/page_404.html", status=404)

# TODO: Show detailed error message
def db_error():    
    response = {
        "status": 404,
        "message": "Error with database. If problem persists, contact software.wbc@gmail.com",
    }
    return JsonResponse(response)  