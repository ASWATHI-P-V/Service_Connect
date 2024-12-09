from django.urls import path
from .views import DealerDetailView, AddDealerView, PaymentRequestListCreateView

urlpatterns = [
    path('dealer-detail/', DealerDetailView.as_view(), name='dealer-detail'),
    path('add-dealer/', AddDealerView.as_view(), name='add-dealer'),
    path('payment-requests/', PaymentRequestListCreateView.as_view(), name='payment-requests'),
]
