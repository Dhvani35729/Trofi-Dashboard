from safe_schedule import SafeScheduler
import time
import stripe
import datetime
from config import db

stripe.api_key = "sk_test_WZJim1CVcSc7WBSKjdRDxJGS"


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
        u'is_active', u'==', True).stream()

    for restaurant in all_restaurants:
        print("Working on restaurant: " + str(restaurant.id))
        res_public_data = restaurant.to_dict()

        hour_ref = db.collection(u'restaurants').document(
            restaurant.id).collection("hours").document(str(hour_id))
        hour_data = hour_ref.get().to_dict()

        all_discounts = hour_data["discounts"]
        final_discount = 0.0
        for discount in sorted(all_discounts):
            if all_discounts[discount]["is_active"] is True:
                final_discount = float(discount.replace("_", "."))
                break

        all_orders = db.collection(u'orders').where(
            u'placed_at', u'>=', today).where(
            u'hour_id', u'==', hour_id).where(
            u'restaurant_id', u'==', restaurant.id).stream()

        for order in all_orders:
            order_ref = db.collection("orders").document(order.id)
            order_data = order.to_dict()
            final_total = round(
                order_data["initial_total"] * (1 - final_discount))
            print("Working on order: " + str(order_data["order_number"]))

            order_ref.update(
                {u'final_discount': final_discount, "final_total": final_total})
            try:
                charge = stripe.Charge.capture(
                    order_data["charge_id"], amount=final_total)
                print("Succesfully captured: " + str(final_total))
            except:
                # throw some error
                return


# run_hourly(21)
def job():
    now = datetime.datetime.now()
    previous_hour = now.hour - 1
    run_hourly(now.hour)


scheduler = SafeScheduler()
scheduler.every().hour.at(':56').do(job)

while True:
    scheduler.run_pending()
    time.sleep(1)
