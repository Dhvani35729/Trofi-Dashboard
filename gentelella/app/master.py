import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

config = {
  "apiKey": "AIzaSyCwgogOI0rJDijj-r97dbWjEinKkrBH1Ok",
  "authDomain": "daydesign-a277f.firebaseapp.com",
  "databaseURL": "https://daydesign-a277f.firebaseio.com",
  "storageBucket": "daydesign-a277f.appspot.com"
}

# firestore config
# Use a service account
cred = credentials.Certificate('../serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def main():
    algo_foods, MAX_DISCOUNT = init_algorithm("trofi-res-test-123k")
    run_algorithm("trofi-res-test-123k", algo_foods, MAX_DISCOUNT)


def init_algorithm(res_public_id):
    algo_foods = []

    all_foods = db.collection(u'foods').where(u'restaurant_id', u'==', res_public_id).stream()
    MAX_DISCOUNT = 100
    for food in all_foods:
        # print(u'{} => {}'.format(food.id, food.to_dict()))
        food_data = food.to_dict()
        sales_price = food_data["sales_price"]

        private_info = db.collection(u'foods').document(food.id).collection(u'private').stream()
        for info in private_info:
            # print(u'{} => {}'.format(info.id, info.to_dict()))
            res_private_id = info.id
            info_data = info.to_dict()
            ingredients_cost = info_data["ingredients_cost"]
            profit_margin = info_data["profit_margin"]

        res_private_ref = db.collection(u'restaurants').document(res_public_id).collection(u'private').document(res_private_id)
        res_private_data = res_private_ref.get().to_dict()
        credit_card_percentage = res_private_data["credit_card_percentage"]
        credit_card_constant = res_private_data["credit_card_constant"]

        # For food.id
        # Got sales_price, ingredients_cost, and profit_margin
        # Trofi Algorithm initialization
        credit_card_fee = sales_price * (credit_card_percentage) + credit_card_constant
        initial_expense_contribution = sales_price - (profit_margin + ingredients_cost + credit_card_fee)

        max_food_discount = initial_expense_contribution / sales_price
        food = {
            "id": food.id,
            "sales_price": sales_price,
            "credit_card_fee": credit_card_fee,
            "initial_expense_contribution": initial_expense_contribution,
            "max_discount": max_food_discount,
        }
        if max_food_discount < MAX_DISCOUNT:
            MAX_DISCOUNT = max_food_discount

        algo_foods.append(food)

    return algo_foods, MAX_DISCOUNT


def run_algorithm(res_public_id, algo_foods, MAX_DISCOUNT):
    print(algo_foods)
    all_hours = db.collection(u'restaurants').document(res_public_id).collection("hours").stream()

    for hour in all_hours:
        # print(u'{} => {}'.format(hour.id, hour.to_dict()))
        hour_data = hour.to_dict()
        needed_contribution = hour_data["payroll"] + hour_data["overhead_cost"]

        # initial_discount = hour_data["initial_discount"]
        initial_discount = hour_data["discounts"][0]["percent_discount"]
        print("FOR HOUR: " + hour.id)
        # generate
        for food in algo_foods:
            print("\n--------------------------------\n")
            percent_discount = initial_discount
            expense_contribution = food["initial_expense_contribution"]
            while percent_discount < MAX_DISCOUNT:
                discount = food["sales_price"] * percent_discount
                expense_contribution -= discount

                print("To unlock a discount of: ", percent_discount)
                print("Item will contribute: ", expense_contribution)

                percent_discount += 0.05

            print("\n--------------------------------\n")


main()