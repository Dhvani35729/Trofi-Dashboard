from django.http import JsonResponse


def user_not_found(user_public_id):
    return JsonResponse({
        "error": {
            "code": "UserNotFound",
            "id": user_public_id,
            "message": "The specified user does not exist",
        }
    })


def get_user_current_order(db, user_public_id, user_private_id):
    user_private_ref = db.collection(u'users').document(
        user_public_id).collection(u'private').document(user_private_id).get()

    user_private_data = user_private_ref.to_dict()
    if user_private_data is None:
        return user_not_found(user_public_id)
