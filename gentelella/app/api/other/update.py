from ..common import api_success, api_db_error


def update_ccf_percentage(db, public_id, uid, body):
    new_ccf_percentage = body["ccf_percentage"]
    res_private_ref = db.collection(u'restaurants').document(public_id).collection(u'private').document(uid)

    try:
        res_private_ref.update({u'credit_card_percentage': new_ccf_percentage})
    except Exception as e:
        return api_db_error(e)

    return api_success()


def update_ccf_constant(db, public_id, uid, body):
    new_ccf_constant = body["ccf_constant"]
    res_private_ref = db.collection(u'restaurants').document(public_id).collection(u'private').document(uid)

    try:
        res_private_ref.update({u'credit_card_constant': new_ccf_constant})
    except Exception as e:
        return api_db_error(e)

    return api_success()
