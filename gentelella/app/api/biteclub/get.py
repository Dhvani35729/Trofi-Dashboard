import requests
import json
from django.http import JsonResponse
from ..common import generic_api_error
api_key = '15MjvqetSuD6DR_iOkUZqBktkUf46W59AeZ3S-5niNe2Wa6xBqbjbmEmrKvTMWw7t7SnbgfMrJxLvwX1P5zxfBCXLF_ml6m4CU64X29YMJsD9zOLlI_ysAqgTasrXXYx'
headers = {'Authorization': 'Bearer %s' % api_key}


def get_yelp_data_from_params(url, params):
    # Making a get request to the API
    req = requests.get(url, params=params, headers=headers)

    # proceed only if the status code is 200
    # print('The status code is {}'.format(req.status_code))
    if req.status_code == 200:
        parsed = json.loads(req.text)
        # printing the text from the response
        # print(json.dumps(parsed, indent=4))

        businesses = parsed["businesses"]

        all_businesses = []
        for business in businesses:
            business_data = {
                "name": business["name"],
                "rating": business["rating"],
                "num_reviews": business["review_count"],
                "address": business["location"]["display_address"],
                "price": business.get("price", ""),
                "categories": list(map(lambda x: x["title"], business["categories"]))
            }
            all_businesses.append(business_data)

        return all_businesses, parsed["total"]
    else:
        return None, 0


def get_all_restaurants():
    url = 'https://api.yelp.com/v3/businesses/search'

    # In the dictionary, term can take values like food, cafes or businesses like McDonalds
    params = {'term': 'restaurants', 'limit': 50,
              'latitude': 43.472012, 'longitude': -80.537752, 'radius': 1000}

    all_restaurants = []
    restaurants, total = get_yelp_data_from_params(url, params)
    all_restaurants += restaurants

    if restaurants and total >= 50:
        params["offset"] = 50
        restaurants, total = get_yelp_data_from_params(url, params)
        if restaurants:
            all_restaurants += restaurants
            return JsonResponse({"list": all_restaurants, "total": len(all_restaurants)})
    elif restaurants:
        return JsonResponse({"list": all_restaurants, "total": len(all_restaurants)})
    else:
        return generic_api_error()
