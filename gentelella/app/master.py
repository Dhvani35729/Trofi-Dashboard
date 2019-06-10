import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from google.cloud.firestore_v1 import ArrayUnion, ArrayRemove

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


def reset_hours(public_id):

    res_ref = db.collection(u'restaurants').document(public_id)

    init_hours_ref = res_ref.collection(u'hours')

    init_0_hours_ref = init_hours_ref.document("0")
    init_1_hours_ref = init_hours_ref.document("1")
    init_2_hours_ref = init_hours_ref.document("2")
    init_3_hours_ref = init_hours_ref.document("3")
    init_4_hours_ref = init_hours_ref.document("4")
    init_5_hours_ref = init_hours_ref.document("5")
    init_6_hours_ref = init_hours_ref.document("6")
    init_7_hours_ref = init_hours_ref.document("7")
    init_8_hours_ref = init_hours_ref.document("8")
    init_9_hours_ref = init_hours_ref.document("9")
    init_10_hours_ref = init_hours_ref.document("10")
    init_11_hours_ref = init_hours_ref.document("11")
    init_12_hours_ref = init_hours_ref.document("12")
    init_13_hours_ref = init_hours_ref.document("13")
    init_14_hours_ref = init_hours_ref.document("14")
    init_15_hours_ref = init_hours_ref.document("15")
    init_16_hours_ref = init_hours_ref.document("16")
    init_17_hours_ref = init_hours_ref.document("17")
    init_18_hours_ref = init_hours_ref.document("18")
    init_19_hours_ref = init_hours_ref.document("19")
    init_20_hours_ref = init_hours_ref.document("20")
    init_21_hours_ref = init_hours_ref.document("21")
    init_22_hours_ref = init_hours_ref.document("22")
    init_23_hours_ref = init_hours_ref.document("23")

    batch = db.batch()

    batch.set(init_0_hours_ref, {
        "start_id": 0,
        "payroll": 0,
        "overhead_cost": 0,
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "contributions": {},
        "foods_active": []
    })
    batch.set(init_1_hours_ref, {
        "start_id": 1,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_2_hours_ref, {
        "start_id": 2,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_3_hours_ref, {
        "start_id": 3,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_4_hours_ref, {
        "start_id": 4,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_5_hours_ref, {
        "start_id": 5,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_6_hours_ref, {
        "start_id": 6,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_7_hours_ref, {
        "start_id": 7,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_8_hours_ref, {
        "start_id": 8,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_9_hours_ref, {
        "start_id": 9,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_10_hours_ref, {
        "start_id": 10,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_11_hours_ref, {
        "start_id": 11,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_12_hours_ref, {
        "start_id": 12,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_13_hours_ref, {
        "start_id": 13,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_14_hours_ref, {
        "start_id": 14,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_15_hours_ref, {
        "start_id": 15,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_16_hours_ref, {
        "start_id": 16,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_17_hours_ref, {
        "start_id": 17,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_18_hours_ref, {
        "start_id": 18,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_19_hours_ref, {
        "start_id": 19,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_20_hours_ref, {
        "start_id": 20,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_21_hours_ref, {
        "start_id": 21,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_22_hours_ref, {
        "start_id": 22,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })
    batch.set(init_23_hours_ref, {
        "start_id": 23,
        "payroll": 0,
        "overhead_cost": 0,
        "contributions": {},
        "hour_is_active": False,
        "initial_discount": 0,
        "discounts": {},
        "foods_active": []
    })

    batch.commit()


WORK_ON_RES = "trofi-res-test-123k"


def main():
    # reset_hours(WORK_ON_RES)
    algo_foods, MAX_DISCOUNT = init_algorithm(WORK_ON_RES)
    run_algorithm(WORK_ON_RES, algo_foods, MAX_DISCOUNT)


def init_algorithm(res_public_id):
    algo_foods = []

    all_foods = db.collection(u'foods').where(
        u'restaurant_id', u'==', res_public_id).stream()
    MAX_DISCOUNT = 100
    for food in all_foods:
        # print(u'{} => {}'.format(food.id, food.to_dict()))
        food_data = food.to_dict()
        sales_price = food_data["sales_price"]

        private_info = db.collection(u'foods').document(
            food.id).collection(u'private').stream()
        for info in private_info:
            # print(u'{} => {}'.format(info.id, info.to_dict()))
            res_private_id = info.id
            info_data = info.to_dict()
            ingredients_cost = info_data["ingredients_cost"]
            profit_margin = info_data["profit_margin"]

        res_private_ref = db.collection(u'restaurants').document(
            res_public_id).collection(u'private').document(res_private_id)
        res_private_data = res_private_ref.get().to_dict()
        credit_card_percentage = res_private_data["credit_card_percentage"]
        credit_card_constant = res_private_data["credit_card_constant"]

        # For food.id
        # Got sales_price, ingredients_cost, and profit_margin
        # Trofi Algorithm initialization
        credit_card_fee = sales_price * \
            (credit_card_percentage) + credit_card_constant
        # TEST
        credit_card_fee = 0
        initial_expense_contribution = sales_price - \
            (profit_margin + ingredients_cost + credit_card_fee)

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
    # print(algo_foods)
    all_hours = db.collection(u'restaurants').document(
        res_public_id).collection("hours").stream()

    batch = db.batch()

    for hour in all_hours:
        all_hour_discounts = {}
        all_food_contributions = {}
        # print(u'{} => {}'.format(hour.id, hour.to_dict()))
        hour_data = hour.to_dict()
        needed_contribution = hour_data["payroll"] + hour_data["overhead_cost"]

        # initial_discount = hour_data["initial_discount"]
        initial_discount = hour_data["initial_discount"]
        print("FOR HOUR: " + hour.id)

        percent_discount = 0.0
        while percent_discount < MAX_DISCOUNT:
            if initial_discount > 0:
                print(percent_discount)
            active = True if initial_discount > 0 and percent_discount == initial_discount else False

            hour_discount = {
                "is_active": active,
                "current_contributed": 0,
            }
            format_discount = "{:.2f}".format(percent_discount)
            all_hour_discounts[format_discount] = hour_discount

            percent_discount += 0.05
            percent_discount = round(percent_discount, 2)
        # generate
        for food in algo_foods:
            print("\n--------------------------------\n")
            percent_discount = 0.0
            expense_contribution = food["initial_expense_contribution"]
            prev_positive_value = 0.0
            food_contributions = {}
            print("FOR FOOD: " + food["id"])

            while percent_discount < MAX_DISCOUNT:
                discount = food["sales_price"] * percent_discount
                expense_contribution = food["initial_expense_contribution"] - discount

                # if expense_contribution < 0:
                #     expense_contribution = prev_positive_value
                # else:
                #     prev_positive_value = expense_contribution
                print("To unlock a discount of: ", percent_discount)
                print("Item will contribute: ", expense_contribution)

                format_discount = "{:.2f}".format(percent_discount)
                food_contributions[format_discount] = expense_contribution
                percent_discount += 0.05
                percent_discount = round(percent_discount, 2)

            all_food_contributions[str(food["id"])] = food_contributions

        print(all_food_contributions)
        print(all_hour_discounts)
        hour_ref = db.collection(u'restaurants').document(
            res_public_id).collection("hours").document(hour.id)

        batch.update(
            hour_ref, {u'needed_contribution': needed_contribution})
        batch.update(
            hour_ref, {u'contributions': all_food_contributions})
        batch.update(
            hour_ref, {u'discounts': all_hour_discounts})

    print("\n--------------------------------\n")
    print("Writing to database...")
    batch.commit()
    print("Done!")


main()
