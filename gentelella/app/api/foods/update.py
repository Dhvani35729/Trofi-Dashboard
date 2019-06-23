from ..common import api_success, api_db_error


def update_food_sales_price(db, uid, body):
    food_id = body["food_id"]
    new_sales_price = body["sales_price"]
    food_ref = db.collection(u'foods').document(food_id)

    try:
        food_ref.update({u'sales_price': new_sales_price})
    except Exception as e:
        return api_db_error(e)

    return api_success()


def update_food_profit_margin(db, uid, body):
    food_id = body["food_id"]
    new_profit_margin = body["profit_margin"]
    food_private_ref = db.collection(u'foods').document(food_id).collection(u'private').document(uid)

    try:
        food_private_ref.update({u'profit_margin': new_profit_margin})
    except Exception as e:
        return api_db_error(e)

    return api_success()


def update_food_ingredients_cost(db, uid, body):
    food_id = body["food_id"]
    new_ingredients_cost = body["ingredients_cost"]
    food_private_ref = db.collection(u'foods').document(food_id).collection(u'private').document(uid)

    try:
        food_private_ref.update({u'ingredients_cost': new_ingredients_cost})
    except Exception as e:
        return api_db_error(e)

    return api_success()
