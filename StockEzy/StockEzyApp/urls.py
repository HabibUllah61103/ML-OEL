from django.urls import path
from . import views

urlpatterns = [
    path("", views.customer_signup, name="customer_signup"),
    path("customer_signin", views.customer_signin, name="customer_signin"),
    path(
        "customer_profile/<int:customer_id>",
        views.customer_profile,
        name="customer_profile",
    ),
    path("dashboad_view/<int:customer_id>", views.dashboad_view, name="dashboard_view"),
    path("history_view/<int:customer_id>", views.history_view, name="history_view"),
    # path("license_view>", views.license_view, name="license_view"),
]
