from django.http import JsonResponse

def api_success():
    response = {
        "status": 200,
        "message": "Success!"
    }
    return JsonResponse(response) 


# TODO: Show detailed error message
def api_db_error():    
    response = {
        "status": 404,
        "message": "Error with database. If problem persists, contact software.wbc@gmail.com",
    }
    return JsonResponse(response)  