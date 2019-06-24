from config import db
import json


def main():
    # load menu
    print("Opening file...")
    with open('menu.txt', 'r') as menu:
        print("Parsing file as JSON...")
        food_data = json.loads(menu.read())
        food_list = food_data["list"]
        print("Found: " + str(len(food_list)) + " items")
        for food_item in food_list:
            print("Writing: " + food_item["public"]["name"])
            upload_food_item(food_item)
    print("Finished!")


def upload_food_item(food_item):
    try:
        new_food_ref = db.collection(u'foods').document()
        new_food_ref.set(food_item["public"])
        private_ref = new_food_ref.collection(u'private').document()
        private_ref.set(food_item["private"])
    except:
        print("DB Error!")


main()
