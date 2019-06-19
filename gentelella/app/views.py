from django.shortcuts import redirect

from .constants import HOME_PAGE, HOME_PAGE_LOGGED_OUT
from .auth.utils import logged_in

# API Views
from .api.base import (
    api_hours,
    api_orders,
    api_foods,
    api_user_card,
    api_user_cards,
    api_user_order,
    api_user_all_orders,
    api_user_current_order,
    api_restaurants_hour,
    api_restaurant_hour,
    api_restaurant_menu,
    api_others
)

# Page Views
from .auth.views import sign_up, sign_in, logout
from .incoming.views import incoming
from .history.views import history
from .manage.views import manage


def index(request):
    if logged_in(request):
        response = redirect(HOME_PAGE)
    else:
        response = redirect(HOME_PAGE_LOGGED_OUT)
    return response
