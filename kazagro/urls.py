from django.urls import path, include
from .views import *

urlpatterns = [
    path("", base),
    path("<str:razdel>", index, name="index"),
    path("add/add_row", addRow, name="add")
]
