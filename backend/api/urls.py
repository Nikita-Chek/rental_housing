from django.urls import path
from .views import (apartments_all,
                    apartments_page,
                    apartment,
                    mean_by,
                    count_rooms,
                    median_by_year)
from .scrapping.apartments_update import apartments_update
from .scrapping.apartments_insert import apartments_insert
from .scrapping.apartments_update_existing import apartments_update_existing
from .api_help import api_help


urlpatterns = [
    path('', api_help),
    path('apartments/', apartments_all),
    path('apartments/page/<int:pk>/', apartments_page),
    path('apartments/<int:pk>/', apartment),
    path('apartments/update/', apartments_update),
    path('apartments/update/existing/', apartments_update_existing),
    path('apartments/insert/', apartments_insert),
    path('mean_by/<str:period>/', mean_by),
    path('count_rooms/', count_rooms),
    path('median_by_year/', median_by_year),
]