from django.contrib import admin
from .models import OTP, Category, Collar, Customer, CustomerReview, Dealer, District, Franchise_Type, Franchisee, Invoice, Service_Type, ServiceProvider, ServiceRegister, ServiceRequest, State, Subcategory, User, Country_Codes,PaymentRequest,Complaint,Payment, Ad_category,Ad_Management,AdminProfile,IncomeManagement,DeclineServiceModel
from .models import *

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    
    list_display = ('booking_id', 'customer', 'service_provider', 'work_status', 'request_date')
    list_filter = ('work_status', 'acceptance_status', 'reschedule_status')
    search_fields = ('booking_id', 'customer__full_name', 'service_provider__full_name')


admin.site.register(User)
admin.site.register(Customer)
admin.site.register(ServiceProvider)
admin.site.register(Franchisee)
admin.site.register(Franchise_Type)
admin.site.register(Dealer)
admin.site.register(Country_Codes)
admin.site.register(OTP)
admin.site.register(District)
admin.site.register(State)
admin.site.register(ServiceRegister)
admin.site.register(Collar)
admin.site.register(Service_Type)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Invoice)
admin.site.register(CustomerReview)
admin.site.register(PaymentRequest)
admin.site.register(Payment)
admin.site.register(Ad_category)
admin.site.register(Ad_Management)
admin.site.register(AdminProfile)
admin.site.register(IncomeManagement)
admin.site.register(DeclineServiceModel)
admin.site.register(Complaint)

