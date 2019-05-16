from ..config import db


# check if user is logged in
def logged_in(request):
    try:
        return request.session['uid']
    except KeyError:
        return None


def get_res_public_id(uid):
    map_ref = db.collection(u'general').document("trofi-verification").collection(uid).document("map")
    try:
        map_data = map_ref.get().to_dict()
        return map_data["public_id"]
    except Exception as e:
        return None

def is_valid_trofi_code(code):
    code_ref = db.collection(u'general').document(u'trofi-verification')

    try:
        code_data = code_ref.get()
        if code in code_data.to_dict()["accepted_codes_unused"]:
            return True
        else:
            return False
    except Exception as e:
        return None


def should_allow_user_in(public_id, uid):

    res_ref = db.collection(u'restaurants').document(public_id)
    res_private_ref = res_ref.collection(u'private').document(uid)

    try:
        res_private_data = res_private_ref.get().to_dict()
        if res_private_data["allow_in"]:
            return True, res_private_data
        else:
            return False, None
    except Exception as e:
        return None, None