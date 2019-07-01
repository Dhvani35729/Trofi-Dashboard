from django.http import JsonResponse


def get_app_maint(db):

    maint_ref = db.collection(u'general').document(
        u'maint')

    try:
        maint_data = maint_ref.get().to_dict()
        return JsonResponse(maint_data)
    except Exception as e:
        print(u'No such document!')
        return None
