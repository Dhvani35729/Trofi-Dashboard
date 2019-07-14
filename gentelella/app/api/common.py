from django.http import JsonResponse
from ..utils import get_message_from_exception


def api_success():
    response = {
        "status": 200,
        "error": None,
        "message": "Success!"
    }
    return JsonResponse(response)


def generic_api_error():
    return JsonResponse({
        "error": {
            "code": "TrofiAPIError",
            "message": "Unknown error.",
        }
    })

# TODO: Show detailed error message


def api_db_error(e):
    err_msg = ""
    if e is not None:
        err_msg = e
        if len(e.args) > 1:
            err_msg = get_message_from_exception(e)
    response = {
        "status": 404,
        "error": str(err_msg),
        "message": "Error with database. If problem persists, contact software.wbc@gmail.com",
    }
    return JsonResponse(response)
