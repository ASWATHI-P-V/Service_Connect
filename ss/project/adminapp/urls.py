from django.urls import path
from . import views

urlpatterns = [
    path('booking-details/', views.BookingDetailsView.as_view(), name='booking-details'),
    path('franchise-types/', views.FranchiseTypeListCreateView.as_view(), name='franchise_type_list_create'),
    path('franchise-types/edit/', views.FranchiseTypeUpdateView.as_view(), name='franchise_type_update'),
    path('ads/', views.AdListView.as_view(), name='ad-list'),
    path('ads/category/edit/', views.AdCategoryEditView.as_view(), name='ad-category-edit'),
    path('ads/new/', views.AddNewAdView.as_view(), name='add-new-ad'),
    

]
