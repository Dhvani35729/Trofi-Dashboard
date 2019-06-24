from ..config import db


def get_user_public_id(uid):
    map_ref = db.collection(u'general').document(
        "user-verification").collection(uid).document("map")
    try:
        map_data = map_ref.get().to_dict()
        return map_data["public_id"]
    except:
        return None
