from django.urls import path
from bands import views

urlpatterns = [
    path("", views.bands, name="bands"),
    path("band/<int:band_id>", views.band, name="band"),
    path("musician/<int:musician_id>/", views.musician, name="musician"),
    path(
        "musician_restricted/<int:musician_id>",
        views.musician_restricted,
        name="musician_restricted",
    ),
    path("musicians/", views.musicians, name="musicians"),
    path("restricted_page/", views.restricted_page, name="restricted_page"),
]
