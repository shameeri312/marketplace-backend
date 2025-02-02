# URLs
from django.urls import path
from .views import *

app_name = "items"

urlpatterns = [
    path("items/", ItemListView.as_view(), name="all-items"),
    path("items/<int:id>/", ItemDetailView.as_view(), name="single-item"),
    path(
        "items/category/<str:category>/",
        ItemByCategoryView.as_view(),
        name="items-by-category",
    ),
]
