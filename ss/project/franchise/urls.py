from django.urls import path
from . import views

urlpatterns = [
    path('franchise-types/', views.FranchiseTypeListCreateView.as_view(), name='franchise_type_list_create'),
    path('franchise-types/edit/', views.FranchiseTypeUpdateView.as_view(), name='franchise_type_update'),
    path('block-dealer/', views.BlockDealerView.as_view(), name='block-dealer'),
    path('block-service-provider/', views.BlockServiceProviderView.as_view(), name='block-service-provider'),

]

