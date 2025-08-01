from django.urls import path
from .views import join_waitlist, get_stats

urlpatterns = [
    path('join/', join_waitlist),
    # path("createsuperuser/", create_superuser),
    path('stats/', get_stats, name='get_stats'),
]
