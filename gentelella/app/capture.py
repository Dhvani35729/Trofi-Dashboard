from safe_schedule import SafeScheduler
import time
import stripe
import datetime
from config import db
import pytz

stripe.api_key = "sk_test_WZJim1CVcSc7WBSKjdRDxJGS"

# charge = stripe.Charge.capture('ch_1EnH7GFx6ej5bzOr1r4C9wY2', amount=100)

# print(charge)


def run_hourly(hour_id):
    print("Working on hour: " + str(hour_id))

    today_date = datetime.date.today()
    start_day_time = datetime.time(0, 0)
    today = datetime.datetime.combine(today_date, start_day_time)
    LOCAL_TIMEZONE = datetime.datetime.now(
        datetime.timezone.utc).astimezone().tzinfo
    today = today.replace(tzinfo=LOCAL_TIMEZONE)
    print("Today: " + str(today))

    all_restaurants = db.collection(u'restaurants').where(
        u'all_discounts_active', u'==', True).stream()

    for restaurant in all_restaurants:
        print("Working on restaurant: " + str(restaurant.id))
        res_public_data = restaurant.to_dict()

        all_orders = db.collection(u'orders').where(
            u'placed_at', u'>=', today).where(
            u'hour_id', u'==', hour_id).where(
            u'restaurant_id', u'==', restaurant.id).stream()

        for order in all_orders:
            print(order.to_dict()["order_number"])
            print(order.to_dict()["placed_at"])
            # print(order.to_dict()["placed_at"] >= today)


run_hourly(22)
# def job():
#     now = datetime.datetime.now()
#     run_hourly(now.hour)


# scheduler = SafeScheduler()
# scheduler.every().hour.at(':18').do(job)

# while True:
#     scheduler.run_pending()
#     time.sleep(1)
