from django.urls import path
from .views import join_waitlist, create_superuser

urlpatterns = [
    path('join/', join_waitlist),
    path("createsuperuser/", create_superuser),

]
