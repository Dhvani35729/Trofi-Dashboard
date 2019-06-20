import stripe

stripe.api_key = "sk_test_WZJim1CVcSc7WBSKjdRDxJGS"

charge = stripe.Charge.capture('ch_1EnH7GFx6ej5bzOr1r4C9wY2', amount=100)

print(charge)
