
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./daydesign-a277f-firebase-adminsdk-hr01g-6f01b5bf82.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection(u'users').document(u'um5CQ8O7PchNbzxX7C4Um6uQB9J3')

try:
    doc = doc_ref.get()
    print(u'Document data: {}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'No such document!')