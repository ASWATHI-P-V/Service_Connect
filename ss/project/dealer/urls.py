from django.urls import path
from .views import DealerDetailView

urlpatterns = [
    path('dealer-detail/', DealerDetailView.as_view(), name='dealer-detail'),
]
